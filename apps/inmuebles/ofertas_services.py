
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Inmueble, Oferta


@transaction.atomic
def crear_oferta(inmueble_id, formulario):
    """
    Registra una oferta comercial.
    """

    inmueble = (
        Inmueble.objects
        .select_for_update()
        .get(pk=inmueble_id)
    )

    oferta = formulario.save(commit=False)

    oferta.id_inmueble = inmueble

    if Oferta.objects.filter(
        id_inmueble=inmueble,
        modalidad=oferta.modalidad
    ).exists():
        raise ValidationError(
            "El inmueble ya tiene una oferta "
            "de esta modalidad."
        )

    oferta.save()

    return oferta


@transaction.atomic
def actualizar_oferta(oferta_id, formulario):
    """
    Actualiza las condiciones comerciales
    sin cambiar el inmueble ni la modalidad.
    """

    oferta = (
        Oferta.objects
        .select_for_update()
        .get(pk=oferta_id)
    )

    oferta.precio = formulario.cleaned_data["precio"]
    oferta.a_convenir = formulario.cleaned_data["a_convenir"]

    oferta.save(
        update_fields=["precio", "a_convenir"]
    )

    return oferta


@transaction.atomic
def eliminar_oferta(oferta_id):
    """
    Elimina una oferta sin eliminar el inmueble.
    """

    oferta = (
        Oferta.objects
        .select_for_update()
        .get(pk=oferta_id)
    )

    inmueble_id = oferta.id_inmueble_id
    modalidad = oferta.modalidad

    oferta.delete()

    return inmueble_id, modalidad
