from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    """
    Modelo personalizado para los usuarios del sistema.

    Hereda de AbstractUser para utilizar el sistema
    de autenticación, contraseñas y permisos de Django.
    """

    email = models.EmailField(
        unique=True,
        verbose_name="Correo electrónico"
    )

    def __str__(self):
        return self.username
