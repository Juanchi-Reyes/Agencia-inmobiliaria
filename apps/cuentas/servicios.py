
from django.contrib.auth import get_user_model
from django.db import models

Usuario = get_user_model()


def es_ultimo_administrador(usuario):
    """
    Comprueba si es el último administrador
    activo de la aplicación.

    Se consideran administradores:
    - Superusuarios activos.
    - Usuarios activos del grupo Administrador.
    """

    if not usuario.is_active:
        return False

    administradores = (
        Usuario.objects.filter(is_active=True)
        .filter(
            models.Q(is_superuser=True)
            | models.Q(groups__name="Administrador")
        )
        .distinct()
    )

    es_administrador = (
        usuario.is_superuser
        or usuario.groups.filter(
            name="Administrador"
        ).exists()
    )

    return (
        es_administrador
        and administradores.count() <= 1
    )
