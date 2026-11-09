
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import (
    Inmueble,
    Vivienda,
    Caracteristica,
    Estancia,
    InmuebleCaracteristica,
    ViviendaEstancia,
)


@transaction.atomic
def asignar_caracteristica(inmueble_id, caracteristica_id, detalle):

    inmueble = Inmueble.objects.select_for_update().get(
        pk=inmueble_id
    )

    caracteristica = Caracteristica.objects.get(
        pk=caracteristica_id
    )

    if InmuebleCaracteristica.objects.filter(
        id_inmueble_id=inmueble.pk,
        id_caracteristica_id=caracteristica.pk,
    ).exists():
        raise ValidationError(
            "Esta característica ya está asignada al inmueble."
        )

    return InmuebleCaracteristica.objects.create(
        id_inmueble=inmueble,
        id_caracteristica=caracteristica,
        detalle=detalle or None,
    )


@transaction.atomic
def actualizar_caracteristica_asignada(
    inmueble_id,
    caracteristica_id,
    detalle,
):
    inmueble = Inmueble.objects.select_for_update().get(
        pk=inmueble_id
    )

    registro = InmuebleCaracteristica.objects.get(
        id_inmueble_id=inmueble.pk,
        id_caracteristica_id=caracteristica_id,
    )

    registro.detalle = detalle or None
    registro.save(update_fields=["detalle"])

    return registro


@transaction.atomic
def quitar_caracteristica(inmueble_id, caracteristica_id):

    inmueble = Inmueble.objects.select_for_update().get(
        pk=inmueble_id
    )

    eliminados, _ = InmuebleCaracteristica.objects.filter(
        id_inmueble_id=inmueble.pk,
        id_caracteristica_id=caracteristica_id,
    ).delete()

    if not eliminados:
        raise ValidationError(
            "La característica ya no está asignada."
        )


@transaction.atomic
def asignar_estancia(inmueble_id, estancia_id, cantidad):

    inmueble = Inmueble.objects.select_for_update().get(
        pk=inmueble_id
    )

    if inmueble.tipo not in ("PISO", "CASA", "VILLA"):
        raise ValidationError(
            "Solo las viviendas pueden tener estancias."
        )

    vivienda = Vivienda.objects.get(
        pk=inmueble.pk
    )

    estancia = Estancia.objects.get(
        pk=estancia_id
    )

    if ViviendaEstancia.objects.filter(
        id_inmueble_id=vivienda.pk,
        id_estancia_id=estancia.pk,
    ).exists():
        raise ValidationError(
            "Esta estancia ya está registrada en la vivienda."
        )

    if cantidad < 1:
        raise ValidationError(
            "La cantidad debe ser mayor que cero."
        )

    return ViviendaEstancia.objects.create(
        id_inmueble=vivienda,
        id_estancia=estancia,
        cantidad=cantidad,
    )


@transaction.atomic
def actualizar_estancia_asignada(
    inmueble_id,
    estancia_id,
    cantidad,
):
    inmueble = Inmueble.objects.select_for_update().get(
        pk=inmueble_id
    )

    if inmueble.tipo not in ("PISO", "CASA", "VILLA"):
        raise ValidationError(
            "Este inmueble no admite estancias."
        )

    if cantidad < 1:
        raise ValidationError(
            "La cantidad debe ser mayor que cero."
        )

    registro = ViviendaEstancia.objects.get(
        id_inmueble_id=inmueble.pk,
        id_estancia_id=estancia_id,
    )

    registro.cantidad = cantidad
    registro.save(update_fields=["cantidad"])

    return registro


@transaction.atomic
def quitar_estancia(inmueble_id, estancia_id):

    inmueble = Inmueble.objects.select_for_update().get(
        pk=inmueble_id
    )

    eliminados, _ = ViviendaEstancia.objects.filter(
        id_inmueble_id=inmueble.pk,
        id_estancia_id=estancia_id,
    ).delete()

    if not eliminados:
        raise ValidationError(
            "La estancia ya no está registrada."
        )
