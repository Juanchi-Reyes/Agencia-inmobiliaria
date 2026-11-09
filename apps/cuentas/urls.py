
from django.urls import path

from . import views


app_name = "cuentas"


urlpatterns = [
    path(
        "registro/",
        views.registro,
        name="registro"
    ),

    path(
        "login/",
        views.InicioSesionView.as_view(),
        name="login"
    ),

    path(
        "panel/",
        views.panel,
        name="panel"
    ),

    path(
        "panel/administrador/",
        views.panel_administrador,
        name="panel_administrador"
    ),

    path(
        "panel/vendedor/",
        views.panel_vendedor,
        name="panel_vendedor"
    ),

    path(
        "panel/cliente/",
        views.panel_cliente,
        name="panel_cliente"
    ),

    path(
        "logout/",
        views.cerrar_sesion,
        name="logout"
    ),
    
    path(
        "usuarios/",
        views.listar_usuarios,
        name="listar_usuarios"
    ),

    path(
        "usuarios/crear/",
        views.crear_usuario,
        name="crear_usuario"
    ),

    path(
        "usuarios/<int:usuario_id>/editar/",
        views.editar_usuario,
        name="editar_usuario"
    ),

    path(
        "usuarios/<int:usuario_id>/desactivar/",
        views.desactivar_usuario,
        name="desactivar_usuario"
    ),
    
    path(
    "usuarios/<int:usuario_id>/reactivar/",
    views.reactivar_usuario,
    name="reactivar_usuario"
    ),
]

