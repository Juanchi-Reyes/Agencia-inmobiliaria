
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Visita


@transaction.atomic
def crear_visita(formulario):
    """
    Registra una visita con los datos validados.
    """
    return formulario.save()


@transaction.atomic
def actualizar_visita(visita_id, formulario):
    """
    Actualiza una visita existente.
    """

    visita = (
        Visita.objects
        .select_for_update()
        .get(pk=visita_id)
    )

    visita.id_cliente = formulario.cleaned_data["id_cliente"]
    visita.id_inmueble = formulario.cleaned_data["id_inmueble"]
    visita.fecha_hora = formulario.cleaned_data["fecha_hora"]
    visita.comentario = formulario.cleaned_data["comentario"]

    visita.save(update_fields=[
        "id_cliente",
        "id_inmueble",
        "fecha_hora",
        "comentario",
    ])

    return visita


@transaction.atomic
def eliminar_visita(visita_id):
    """
    Elimina una visita sin modificar al cliente
    ni al inmueble relacionado.
    """

    visita = (
        Visita.objects
        .select_for_update()
        .get(pk=visita_id)
    )

    visita.delete()
