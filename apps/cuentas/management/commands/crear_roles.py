
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from apps.inmuebles.models import Inmueble


class Command(BaseCommand):
    help = "Crea los roles y configura sus permisos"

    def handle(self, *args, **options):

        Usuario = get_user_model()

        # Obtener o crear los grupos
        administrador, _ = Group.objects.get_or_create(
            name="Administrador"
        )

        vendedor, _ = Group.objects.get_or_create(
            name="Vendedor"
        )

        cliente, _ = Group.objects.get_or_create(
            name="Cliente"
        )

        # Obtener los tipos de contenido de los modelos
        contenido_usuario = ContentType.objects.get_for_model(
            Usuario
        )

        contenido_inmueble = ContentType.objects.get_for_model(
            Inmueble
        )

        # Permisos de inmuebles
        permisos_inmueble = Permission.objects.filter(
            content_type=contenido_inmueble,
            codename__in=[
                "add_inmueble",
                "change_inmueble",
                "delete_inmueble",
                "view_inmueble",
            ],
        )

        # Permisos de usuarios
        permisos_usuario = Permission.objects.filter(
            content_type=contenido_usuario,
            codename__in=[
                "add_usuario",
                "change_usuario",
                "delete_usuario",
                "view_usuario",
            ],
        )

        # Administrador: permisos completos
        administrador.permissions.set(
            list(permisos_inmueble) +
            list(permisos_usuario)
        )

        # Vendedor: consultar, registrar y modificar inmuebles
        vendedor.permissions.set(
            permisos_inmueble.exclude(
                codename="delete_inmueble"
            )
        )

        # Cliente: consultar inmuebles
        cliente.permissions.set(
            permisos_inmueble.filter(
                codename="view_inmueble"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Roles y permisos configurados correctamente."
            )
        )
