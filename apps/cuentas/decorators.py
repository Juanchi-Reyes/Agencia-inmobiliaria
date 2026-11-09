
from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied

from .roles import obtener_rol


def rol_requerido(*roles_permitidos):

    def decorador(vista):

        @wraps(vista)
        def funcion_protegida(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect_to_login(
                    request.get_full_path()
                )

            rol = obtener_rol(request.user)

            if rol not in roles_permitidos:
                raise PermissionDenied(
                    "No tienes permiso para acceder a este panel."
                )

            return vista(request, *args, **kwargs)

        return funcion_protegida

    return decorador
