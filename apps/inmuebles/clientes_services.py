
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Cliente, Visita


@transaction.atomic
def crear_cliente(formulario):
    return formulario.save()


@transaction.atomic
def actualizar_cliente(cliente_id, formulario):

    cliente = Cliente.objects.select_for_update().get(
        pk=cliente_id
    )

    cliente.nombre = formulario.cleaned_data["nombre"]
    cliente.telefono = formulario.cleaned_data["telefono"]

    cliente.save(update_fields=[
        "nombre",
        "telefono",
    ])

    return cliente


@transaction.atomic
def vincular_usuario(cliente_id, usuario):

    cliente = Cliente.objects.select_for_update().get(
        pk=cliente_id
    )

    if usuario is not None:

        if not usuario.groups.filter(
            name="Cliente"
        ).exists():
            raise ValidationError(
                "Solo puedes vincular cuentas del rol Cliente."
            )

        ocupado = Cliente.objects.filter(
            usuario=usuario
        ).exclude(
            pk=cliente.pk
        ).exists()

        if ocupado:
            raise ValidationError(
                "Esta cuenta ya está vinculada a otro cliente."
            )

    cliente.usuario = usuario
    cliente.save(update_fields=["usuario"])

    return cliente


@transaction.atomic
def eliminar_cliente(cliente_id):

    cliente = Cliente.objects.select_for_update().get(
        pk=cliente_id
    )

    if Visita.objects.filter(
        id_cliente_id=cliente.pk
    ).exists():
        raise ValidationError(
            "No puedes eliminar este cliente porque "
            "tiene visitas registradas."
        )

    nombre = cliente.nombre
    cliente.delete()

    return nombre
