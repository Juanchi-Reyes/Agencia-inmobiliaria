
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Inmueble, Propietario


@transaction.atomic
def crear_propietario(formulario):
    """
    Registra un nuevo propietario.
    """
    return formulario.save()


@transaction.atomic
def actualizar_propietario(propietario_id, formulario):
    """
    Actualiza nombre y teléfono de un propietario.
    """

    propietario = (
        Propietario.objects
        .select_for_update()
        .get(pk=propietario_id)
    )

    propietario.nombre = formulario.cleaned_data["nombre"]
    propietario.telefono = formulario.cleaned_data["telefono"]

    propietario.save(
        update_fields=["nombre", "telefono"]
    )

    return propietario


@transaction.atomic
def eliminar_propietario(propietario_id):
    """
    Elimina un propietario únicamente cuando
    no tiene inmuebles asociados.
    """

    propietario = (
        Propietario.objects
        .select_for_update()
        .get(pk=propietario_id)
    )

    tiene_inmuebles = Inmueble.objects.filter(
        id_propietario_id=propietario.pk
    ).exists()

    if tiene_inmuebles:
        raise ValidationError(
            "No puedes eliminar este propietario porque "
            "tiene inmuebles asociados."
        )

    nombre = propietario.nombre

    propietario.delete()

    return nombre
