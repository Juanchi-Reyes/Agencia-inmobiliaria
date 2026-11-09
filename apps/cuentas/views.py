
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from apps.inmuebles.models import Cliente, Inmueble, Propietario

from .decorators import rol_requerido
from .forms import RegistroUsuarioForm
from .roles import obtener_rol

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from .forms import (CrearUsuarioAdminForm, EditarUsuarioAdminForm,)

from .servicios import es_ultimo_administrador

Usuario = get_user_model()

def registro(request):

    if request.user.is_authenticated:
        return redirect("cuentas:panel")

    if request.method == "POST":
        formulario = RegistroUsuarioForm(request.POST)

        if formulario.is_valid():

            with transaction.atomic():

                # 1. Crear la cuenta de usuario
                usuario = formulario.save()

                # 2. Asignar el grupo Cliente
                grupo_cliente = Group.objects.get(
                    name="Cliente"
                )

                usuario.groups.add(grupo_cliente)

                # 3. Construir el nombre completo
                nombre_completo = (
                    f"{usuario.first_name} {usuario.last_name}"
                ).strip()

                # 4. Crear el perfil comercial
                Cliente.objects.create(
                    usuario=usuario,
                    nombre=nombre_completo,
                    telefono=formulario.cleaned_data["telefono"]
                )

            # 5. Iniciar sesión
            login(request, usuario)

            messages.success(
                request,
                "Tu cuenta fue creada correctamente."
            )

            return redirect("cuentas:panel")

    else:
        formulario = RegistroUsuarioForm()

    return render(
        request,
        "cuentas/registro.html",
        {"formulario": formulario}
    )


class InicioSesionView(LoginView):
    template_name = "cuentas/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("cuentas:panel")




@login_required
def panel(request):

    rol = obtener_rol(request.user)

    if rol == "Administrador":
        return redirect("cuentas:panel_administrador")

    if rol == "Vendedor":
        return redirect("cuentas:panel_vendedor")

    if rol == "Cliente":
        return redirect("cuentas:panel_cliente")

    return render(
        request,
        "cuentas/sin_rol.html",
        status=403
    )


@rol_requerido("Administrador")
def panel_administrador(request):

    total_propietarios = Propietario.objects.count()
    total_clientes = Cliente.objects.count()
    contexto = {
        "total_usuarios": (
            request.user.__class__.objects.count()
        ),
        "total_clientes": total_clientes,
        "total_inmuebles": Inmueble.objects.count(),
        "total_propietarios": total_propietarios,
        "es_administrador": True,
    }
    return render(
        request,
        "cuentas/panel_administrador.html",
        contexto
    )


@rol_requerido("Vendedor")
def panel_vendedor(request):

    total_clientes = Cliente.objects.count()
    contexto = {
        "total_inmuebles": Inmueble.objects.count(),
        "total_propietarios": Propietario.objects.count(),
        "total_clientes": total_clientes,
        "es_vendedor": True,
    }
    return render(
        request,
        "cuentas/panel_vendedor.html",
        contexto
    )


@rol_requerido("Cliente")
def panel_cliente(request):

    cliente = Cliente.objects.filter(
        usuario=request.user
    ).first()

    contexto = {
        "cliente": cliente,
        "total_inmuebles": Inmueble.objects.count(),
    }

    return render(
        request,
        "cuentas/panel_cliente.html",
        contexto
    )


@login_required
@require_POST
def cerrar_sesion(request):
    from django.contrib.auth import logout

    logout(request)

    messages.success(
        request,
        "Has cerrado sesión correctamente."
    )

    return redirect("cuentas:login")


@permission_required(
    "cuentas.view_usuario",
    raise_exception=True
)
def listar_usuarios(request):

    usuarios = (
        Usuario.objects
        .prefetch_related("groups")
        .order_by("id")
    )

    return render(
        request,
        "cuentas/usuarios/listar.html",
        {"usuarios": usuarios}
    )


@permission_required(
    "cuentas.add_usuario",
    raise_exception=True
)
def crear_usuario(request):

    if request.method == "POST":
        formulario = CrearUsuarioAdminForm(
            request.POST
        )

        if formulario.is_valid():

            with transaction.atomic():

                usuario = formulario.save(
                    commit=False
                )

                usuario.is_staff = False
                usuario.is_superuser = False
                usuario.save()

                rol = formulario.cleaned_data["rol"]

                grupo = Group.objects.get(
                    name=rol
                )

                usuario.groups.set([grupo])

                if rol == "Cliente":

                    nombre_completo = (
                        f"{usuario.first_name} "
                        f"{usuario.last_name}"
                    ).strip()

                    Cliente.objects.create(
                        usuario=usuario,
                        nombre=nombre_completo,
                    )

            messages.success(
                request,
                "Usuario creado correctamente."
            )

            return redirect(
                "cuentas:listar_usuarios"
            )

    else:
        formulario = CrearUsuarioAdminForm()

    return render(
        request,
        "cuentas/usuarios/formulario.html",
        {
            "formulario": formulario,
            "titulo": "Crear usuario",
        }
    )


@permission_required(
    "cuentas.change_usuario",
    raise_exception=True
)
def editar_usuario(request, usuario_id):

    usuario = get_object_or_404(
        Usuario,
        pk=usuario_id
    )

    if usuario.is_superuser:
        messages.error(
            request,
            "Las cuentas de superusuario no pueden modificarse desde este módulo."
        )
        return redirect("cuentas:listar_usuarios")

    if request.method == "POST":
        formulario = EditarUsuarioAdminForm(
            request.POST,
            instance=usuario
        )

        if formulario.is_valid():
            nuevo_rol = formulario.cleaned_data["rol"]

            if (
                nuevo_rol != "Administrador"
                and es_ultimo_administrador(usuario)
            ):
                formulario.add_error(
                    "rol",
                    "No puedes retirar el rol del último administrador activo."
                )
            else:
                with transaction.atomic():

                    usuario = formulario.save()

                    rol = formulario.cleaned_data["rol"]

                    grupo = Group.objects.get(
                        name=rol
                    )

                    usuario.groups.set([grupo])

                    if rol == "Cliente":

                        nombre_completo = (
                            f"{usuario.first_name} "
                            f"{usuario.last_name}"
                        ).strip()

                        Cliente.objects.update_or_create(
                            usuario=usuario,
                            defaults={
                                "nombre": nombre_completo,
                            }
                        )

                messages.success(
                    request,
                    "Usuario actualizado correctamente."
                )

                return redirect(
                    "cuentas:listar_usuarios"
                )

    else:
        rol_actual = (
            usuario.groups.values_list(
                "name",
                flat=True
            ).first()
        )

        formulario = EditarUsuarioAdminForm(
            instance=usuario,
            initial={"rol": rol_actual}
        )

    return render(
        request,
        "cuentas/usuarios/formulario.html",
        {
            "formulario": formulario,
            "titulo": "Editar usuario",
        }
    )


@permission_required(
    "cuentas.delete_usuario",
    raise_exception=True
)
@require_POST
def desactivar_usuario(request, usuario_id):

    usuario = get_object_or_404(
        Usuario,
        pk=usuario_id
    )

    if usuario.pk == request.user.pk:
        messages.error(
            request,
            "No puedes desactivar tu propia cuenta."
        )

        return redirect(
            "cuentas:listar_usuarios"
        )

    if usuario.is_superuser:
        messages.error(
            request,
            "No se puede desactivar un superusuario desde este módulo."
        )

        return redirect(
            "cuentas:listar_usuarios"
        )

    if es_ultimo_administrador(usuario):
        messages.error(
            request,
            "No puedes desactivar el último administrador activo."
        )
        return redirect("cuentas:listar_usuarios")

    usuario.is_active = False
    usuario.save(update_fields=["is_active"])

    messages.success(
        request,
        "Usuario desactivado correctamente."
    )

    return redirect(
        "cuentas:listar_usuarios"
    )


@permission_required(
    "cuentas.change_usuario",
    raise_exception=True
)
@require_POST
def reactivar_usuario(request, usuario_id):

    usuario = get_object_or_404(
        Usuario,
        pk=usuario_id
    )

    if usuario.is_superuser:
        messages.error(
            request,
            "No puedes modificar superusuarios desde este módulo."
        )
        return redirect("cuentas:listar_usuarios")

    if usuario.is_active:
        messages.info(
            request,
            "Esta cuenta ya se encuentra activa."
        )
        return redirect("cuentas:listar_usuarios")

    usuario.is_active = True
    usuario.save(update_fields=["is_active"])

    messages.success(
        request,
        "Usuario reactivado correctamente."
    )

    return redirect("cuentas:listar_usuarios")

