
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


Usuario = get_user_model()

ROLES = [
    ("Cliente", "Cliente"),
    ("Vendedor", "Vendedor"),
    ("Administrador", "Administrador"),
]

class RegistroUsuarioForm(UserCreationForm):

    first_name = forms.CharField(
        label="Nombre",
        max_length=150,
        required=True
    )

    last_name = forms.CharField(
        label="Apellido",
        max_length=150,
        required=True
    )

    email = forms.EmailField(
        label="Correo electrónico",
        required=True
    )

    telefono = forms.CharField(
        label="Teléfono",
        max_length=25,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ej. 3001234567",
                "autocomplete": "tel",
            }
        ),
    )

    class Meta:
        model = Usuario

        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "telefono",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Este correo electrónico ya está registrado."
            )

        return email

    def clean_telefono(self):
        telefono = self.cleaned_data["telefono"].strip()

        if telefono:
            import re

            if not re.fullmatch(r"\+?[0-9 ]{7,25}", telefono):
                raise forms.ValidationError(
                    "Ingresa un número de teléfono válido."
                )

        return telefono

class CrearUsuarioAdminForm(UserCreationForm):

    rol = forms.ChoiceField(
        choices=ROLES,
        label="Rol del usuario"
    )

    class Meta:
        model = Usuario

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if Usuario.objects.filter(
            email__iexact=email
        ).exists():
            raise forms.ValidationError(
                "Este correo ya está registrado."
            )

        return email

    def clean(self):
        datos = super().clean()

        rol = datos.get("rol")

        if rol == "Cliente":
            if not datos.get("first_name"):
                self.add_error(
                    "first_name",
                    "El nombre es obligatorio."
                )

            if not datos.get("last_name"):
                self.add_error(
                    "last_name",
                    "El apellido es obligatorio."
                )

        return datos


class EditarUsuarioAdminForm(forms.ModelForm):

    rol = forms.ChoiceField(
        choices=ROLES,
        label="Rol del usuario"
    )

    class Meta:
        model = Usuario

        fields = [
            "first_name",
            "last_name",
            "email",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if Usuario.objects.filter(
            email__iexact=email
        ).exclude(
            pk=self.instance.pk
        ).exists():
            raise forms.ValidationError(
                "Este correo ya está registrado."
            )

        return email
