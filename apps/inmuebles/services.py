from django.db import connection, transaction
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import (
    Inmueble,
    Vivienda,
    Piso,
    Casa,
    Villa,
    Local,
    Visita,
)


@transaction.atomic
def crear_inmueble(datos_generales, datos_especificos):
    """
    Crea un inmueble y su especialización.

    Si falla alguna inserción, se revierte
    toda la transacción.
    """

    inmueble = datos_generales.save(commit=False)
    tipo = inmueble.tipo

    if tipo not in ("PISO", "CASA", "VILLA", "LOCAL"):
        raise ValueError("Tipo de inmueble no válido.")

    # Validación defensiva adicional
    if tipo == "VILLA" and inmueble.id_zona_id is not None:
        raise ValueError(
            "Una villa no puede tener zona asignada."
        )

    # 1. Guardar inmueble principal
    inmueble.save()

    # 2. Guardar especialización
    if tipo in ("PISO", "CASA", "VILLA"):

        vivienda = Vivienda.objects.create(
            id_inmueble=inmueble,
            tipo=tipo
        )

        if tipo == "PISO":
            Piso.objects.create(
                id_inmueble=vivienda,
                tipo="PISO",
                estado=datos_especificos["estado"]
            )

        elif tipo == "CASA":
            Casa.objects.create(
                id_inmueble=vivienda,
                tipo="CASA"
            )

        elif tipo == "VILLA":
            Villa.objects.create(
                id_inmueble=vivienda,
                tipo="VILLA",
                superficie_parcela_m2=datos_especificos[
                    "superficie_parcela_m2"
                ],
                urbanizacion=datos_especificos["urbanizacion"]
            )

    elif tipo == "LOCAL":
        Local.objects.create(
            id_inmueble=inmueble,
            tipo="LOCAL",
            numero_puertas=datos_especificos.get(
                "numero_puertas"
            ),
            es_diafano=datos_especificos.get(
                "es_diafano"
            ),
            esta_acondicionado=datos_especificos.get(
                "esta_acondicionado"
            ),
        )

    return inmueble


@transaction.atomic
def actualizar_inmueble(
    inmueble_id,
    formulario_general,
    datos_especificos
):
    """
    Actualiza un inmueble y sus datos específicos
    dentro de una única transacción.
    """

    # Bloquear el registro mientras se actualiza.
    inmueble = Inmueble.objects.select_for_update().get(
        pk=inmueble_id
    )

    # Asegurar que el formulario corresponde al inmueble.
    if formulario_general.instance.pk != inmueble.pk:
        raise ValidationError(
            "El formulario no corresponde al inmueble."
        )

    tipo = inmueble.tipo

    # No permitir modificaciones del tipo.
    if tipo not in ("PISO", "CASA", "VILLA", "LOCAL"):
        raise ValidationError(
            "El inmueble tiene un tipo no válido."
        )

    # Copiar únicamente los campos generales editables.
    campos_editables = [
        "referencia",
        "direccion",
        "superficie_m2",
        "descripcion",
        "id_propietario",
        "id_oficina_gestion",
        "id_oficina_llaves",
        "id_zona",
    ]

    for campo in campos_editables:
        setattr(
            inmueble,
            campo,
            formulario_general.cleaned_data[campo]
        )

    if tipo == "VILLA" and inmueble.id_zona_id is not None:
        raise ValidationError(
            "Una villa no puede tener zona asignada."
        )

    # Guardar datos generales.
    inmueble.save(update_fields=campos_editables)

    # Actualizar únicamente la especialización existente.
    if tipo == "PISO":

        piso = Piso.objects.select_for_update().get(
            id_inmueble_id=inmueble.pk,
            tipo="PISO"
        )

        piso.estado = datos_especificos["estado"]
        piso.save(update_fields=["estado"])

    elif tipo == "CASA":

        # La casa no tiene campos específicos adicionales.
        # Verificamos que su registro exista.
        Casa.objects.get(
            id_inmueble_id=inmueble.pk,
            tipo="CASA"
        )

    elif tipo == "VILLA":

        villa = Villa.objects.select_for_update().get(
            id_inmueble_id=inmueble.pk,
            tipo="VILLA"
        )

        villa.superficie_parcela_m2 = (
            datos_especificos["superficie_parcela_m2"]
        )
        villa.urbanizacion = datos_especificos["urbanizacion"]

        villa.save(update_fields=[
            "superficie_parcela_m2",
            "urbanizacion",
        ])

    elif tipo == "LOCAL":

        local = Local.objects.select_for_update().get(
            id_inmueble_id=inmueble.pk,
            tipo="LOCAL"
        )

        local.numero_puertas = datos_especificos.get(
            "numero_puertas"
        )
        local.es_diafano = datos_especificos.get(
            "es_diafano"
        )
        local.esta_acondicionado = datos_especificos.get(
            "esta_acondicionado"
        )

        local.save(update_fields=[
            "numero_puertas",
            "es_diafano",
            "esta_acondicionado",
        ])

    return inmueble


@transaction.atomic
def eliminar_inmueble(inmueble_id):
    """
    Elimina físicamente un inmueble.

    Reglas:
    - Bloquea el inmueble durante la operación.
    - Impide eliminar inmuebles con visitas.
    - Delega las cascadas a MariaDB.
    - Revierte la operación ante errores.
    """

    inmueble = (
        Inmueble.objects
        .select_for_update()
        .get(pk=inmueble_id)
    )

    referencia = inmueble.referencia

    # Verificar visitas relacionadas.
    tiene_visitas = Visita.objects.filter(
        id_inmueble_id=inmueble.pk
    ).exists()

    if tiene_visitas:
        raise ValidationError(
            "No se puede eliminar este inmueble porque "
            "tiene visitas registradas."
        )

    # El esquema SQL ya define las cascadas.
    # Usamos DELETE directo para que MariaDB las ejecute.
    with connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM inmueble WHERE id_inmueble = %s",
            [inmueble.pk]
        )

        if cursor.rowcount != 1:
            raise ValidationError(
                "No fue posible eliminar el inmueble."
            )

    return referencia

