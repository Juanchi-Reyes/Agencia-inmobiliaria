
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Oferta

from .models import (
    Cliente,
    Inmueble,
    Propietario,
    Oficina,
    Zona,
    TIPOS_INMUEBLE,
    ESTADOS_PISO,
    Caracteristica,
    Estancia,
    InmuebleCaracteristica,
    ViviendaEstancia,
    Visita,
)


class CrearInmuebleForm(forms.ModelForm):

    tipo = forms.ChoiceField(
        choices=[("", "Seleccione un tipo")] + TIPOS_INMUEBLE,
        label="Tipo de inmueble"
    )

    class Meta:
        model = Inmueble

        fields = [
            "referencia",
            "tipo",
            "direccion",
            "superficie_m2",
            "descripcion",
            "id_propietario",
            "id_oficina_gestion",
            "id_oficina_llaves",
            "id_zona",
        ]

        labels = {
            "referencia": "Referencia",
            "direccion": "Dirección",
            "superficie_m2": "Superficie (m²)",
            "descripcion": "Descripción",
            "id_propietario": "Propietario",
            "id_oficina_gestion": "Oficina de gestión",
            "id_oficina_llaves": "Oficina de llaves",
            "id_zona": "Zona",
        }

        widgets = {
            "referencia": forms.TextInput(attrs={
                "placeholder": "Ej. INM-1005"
            }),
            "direccion": forms.TextInput(attrs={
                "placeholder": "Dirección completa"
            }),
            "superficie_m2": forms.NumberInput(attrs={
                "min": "0.01",
                "step": "0.01"
            }),
            "descripcion": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Describe el inmueble"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        relaciones = {
            "id_propietario": Propietario.objects.order_by("nombre"),
            "id_oficina_gestion": Oficina.objects.order_by("nombre"),
            "id_oficina_llaves": Oficina.objects.order_by("nombre"),
            "id_zona": Zona.objects.order_by("nombre"),
        }

        for nombre, queryset in relaciones.items():
            campo = self.fields[nombre]
            campo.queryset = queryset
            campo.label_from_instance = lambda obj: obj.nombre

        self.fields["id_propietario"].empty_label = "Seleccione un propietario"
        self.fields["id_oficina_gestion"].empty_label = "Seleccione una oficina"
        self.fields["id_oficina_llaves"].empty_label = "Sin asignar"
        self.fields["id_zona"].empty_label = "Sin asignar"

    def clean_referencia(self):
        referencia = self.cleaned_data["referencia"].strip()

        if Inmueble.objects.filter(
            referencia=referencia
        ).exists():
            raise ValidationError(
                "Ya existe un inmueble con esta referencia."
            )

        return referencia

    def clean_superficie_m2(self):
        superficie = self.cleaned_data["superficie_m2"]

        if superficie <= 0:
            raise ValidationError(
                "La superficie debe ser mayor que cero."
            )

        return superficie

    def clean(self):
        datos = super().clean()

        if datos.get("tipo") == "VILLA" and datos.get("id_zona"):
            self.add_error(
                "id_zona",
                "Una villa no puede tener zona asignada."
            )

        return datos


class PisoForm(forms.Form):

    estado = forms.ChoiceField(
        label="Estado del piso",
        choices=[("", "Seleccione un estado")] + ESTADOS_PISO
    )


class CasaForm(forms.Form):
    """
    Las casas no tienen campos específicos adicionales.
    """
    pass


class VillaForm(forms.Form):

    superficie_parcela_m2 = forms.DecimalField(
        label="Superficie de la parcela (m²)",
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            "min": "0.01",
            "step": "0.01"
        })
    )

    urbanizacion = forms.CharField(
        label="Urbanización",
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Nombre de la urbanización"
        })
    )


class LocalForm(forms.Form):

    OPCIONES_BOOLEANAS = [
        ("", "Sin especificar"),
        ("1", "Sí"),
        ("0", "No"),
    ]

    numero_puertas = forms.IntegerField(
        label="Número de puertas",
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={"min": "0"})
    )

    es_diafano = forms.TypedChoiceField(
        label="¿Es diáfano?",
        choices=OPCIONES_BOOLEANAS,
        coerce=lambda valor: {
            "1": True,
            "0": False,
            "": None,
        }[valor],
        empty_value=None,
        required=False
    )

    esta_acondicionado = forms.TypedChoiceField(
        label="¿Está acondicionado?",
        choices=OPCIONES_BOOLEANAS,
        coerce=lambda valor: {
            "1": True,
            "0": False,
            "": None,
        }[valor],
        empty_value=None,
        required=False
    )


FORMULARIOS_TIPO = {
    "PISO": PisoForm,
    "CASA": CasaForm,
    "VILLA": VillaForm,
    "LOCAL": LocalForm,
}


class EditarInmuebleForm(forms.ModelForm):
    """
    Permite editar los datos generales de un inmueble.

    El tipo no se incluye porque no puede modificarse
    después de registrar la propiedad.
    """

    class Meta:
        model = Inmueble

        fields = [
            "referencia",
            "direccion",
            "superficie_m2",
            "descripcion",
            "id_propietario",
            "id_oficina_gestion",
            "id_oficina_llaves",
            "id_zona",
        ]

        labels = {
            "referencia": "Referencia",
            "direccion": "Dirección",
            "superficie_m2": "Superficie (m²)",
            "descripcion": "Descripción",
            "id_propietario": "Propietario",
            "id_oficina_gestion": "Oficina de gestión",
            "id_oficina_llaves": "Oficina de llaves",
            "id_zona": "Zona",
        }

        widgets = {
            "referencia": forms.TextInput(attrs={
                "placeholder": "Ej. INM-1005"
            }),
            "direccion": forms.TextInput(attrs={
                "placeholder": "Dirección completa"
            }),
            "superficie_m2": forms.NumberInput(attrs={
                "min": "0.01",
                "step": "0.01"
            }),
            "descripcion": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Descripción del inmueble"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        relaciones = {
            "id_propietario": Propietario.objects.order_by("nombre"),
            "id_oficina_gestion": Oficina.objects.order_by("nombre"),
            "id_oficina_llaves": Oficina.objects.order_by("nombre"),
            "id_zona": Zona.objects.order_by("nombre"),
        }

        for nombre, queryset in relaciones.items():
            self.fields[nombre].queryset = queryset
            self.fields[nombre].label_from_instance = (
                lambda obj: obj.nombre
            )

        self.fields["id_propietario"].empty_label = (
            "Seleccione un propietario"
        )
        self.fields["id_oficina_gestion"].empty_label = (
            "Seleccione una oficina"
        )
        self.fields["id_oficina_llaves"].empty_label = (
            "Sin asignar"
        )
        self.fields["id_zona"].empty_label = "Sin asignar"

        # La base de datos no permite zonas en villas.
        if self.instance.pk and self.instance.tipo == "VILLA":
            self.fields["id_zona"].disabled = True

    def clean_referencia(self):
        referencia = self.cleaned_data["referencia"].strip()

        duplicado = Inmueble.objects.filter(
            referencia=referencia
        ).exclude(
            pk=self.instance.pk
        ).exists()

        if duplicado:
            raise ValidationError(
                "Ya existe otro inmueble con esta referencia."
            )

        return referencia

    def clean_superficie_m2(self):
        superficie = self.cleaned_data["superficie_m2"]

        if superficie <= 0:
            raise ValidationError(
                "La superficie debe ser mayor que cero."
            )

        return superficie

    def clean(self):
        datos = super().clean()

        if (
            self.instance.tipo == "VILLA"
            and datos.get("id_zona") is not None
        ):
            self.add_error(
                "id_zona",
                "Las villas no pueden tener zona asignada."
            )

        return datos


class OfertaForm(forms.ModelForm):
    """
    Formulario para crear y editar ofertas comerciales.
    """

    class Meta:
        model = Oferta

        fields = [
            "modalidad",
            "precio",
            "a_convenir",
        ]

        labels = {
            "modalidad": "Modalidad comercial",
            "precio": "Precio (COP)",
            "a_convenir": "Precio a convenir",
        }

        widgets = {
            "modalidad": forms.Select(),
            "precio": forms.NumberInput(attrs={
                "min": "0",
                "step": "0.01",
                "placeholder": "Ej. 320000000",
            }),
            "a_convenir": forms.CheckboxInput(),
        }

    def __init__(self, *args, inmueble=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.inmueble = inmueble

        self.fields["modalidad"].choices = [
            ("", "Seleccione una modalidad"),
            ("VENTA", "Venta"),
            ("ALQUILER", "Alquiler"),
        ]

        self.fields["precio"].required = False

        # No permitir modificar la modalidad al editar.
        if self.instance.pk:
            self.fields["modalidad"].disabled = True

        # En creación, ocultar las modalidades ya utilizadas.
        elif inmueble is not None:
            existentes = set(
                Oferta.objects.filter(
                    id_inmueble=inmueble
                ).values_list("modalidad", flat=True)
            )

            self.fields["modalidad"].choices = [
                ("", "Seleccione una modalidad")
            ] + [
                (codigo, nombre)
                for codigo, nombre in [
                    ("VENTA", "Venta"),
                    ("ALQUILER", "Alquiler"),
                ]
                if codigo not in existentes
            ]

    def clean_precio(self):
        precio = self.cleaned_data.get("precio")

        if precio is not None and precio < 0:
            raise ValidationError(
                "El precio no puede ser negativo."
            )

        return precio

    def clean(self):
        datos = super().clean()

        modalidad = datos.get("modalidad")
        precio = datos.get("precio")
        a_convenir = datos.get("a_convenir", False)

        if not modalidad:
            return datos

        if a_convenir:
            if modalidad != "VENTA":
                self.add_error(
                    "a_convenir",
                    "La opción a convenir solo está "
                    "disponible para ofertas de venta."
                )

            if precio is not None:
                self.add_error(
                    "precio",
                    "Cuando el precio es a convenir, "
                    "debe dejar este campo vacío."
                )

        elif precio is None:
            self.add_error(
                "precio",
                "Debes ingresar un precio o marcar "
                "la opción a convenir."
            )

        # Evitar duplicar la modalidad de un inmueble.
        if self.inmueble is not None:
            duplicada = Oferta.objects.filter(
                id_inmueble=self.inmueble,
                modalidad=modalidad
            )

            if self.instance.pk:
                duplicada = duplicada.exclude(
                    pk=self.instance.pk
                )

            if duplicada.exists():
                self.add_error(
                    "modalidad",
                    "Este inmueble ya tiene una oferta "
                    "de esa modalidad."
                )

        return datos


class PropietarioForm(forms.ModelForm):
    """
    Formulario para registrar y editar propietarios.
    """

    class Meta:
        model = Propietario

        fields = [
            "nombre",
            "telefono",
        ]

        labels = {
            "nombre": "Nombre completo",
            "telefono": "Teléfono de contacto",
        }

        widgets = {
            "nombre": forms.TextInput(attrs={
                "placeholder": "Nombre completo del propietario",
                "maxlength": "150",
                "autocomplete": "name",
            }),
            "telefono": forms.TextInput(attrs={
                "placeholder": "Número de contacto",
                "autocomplete": "tel",
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()

        if len(nombre) < 3:
            raise ValidationError(
                "El nombre debe tener al menos 3 caracteres."
            )

        return nombre

    def clean_telefono(self):
        telefono = self.cleaned_data["telefono"].strip()

        if not telefono:
            raise ValidationError(
                "Debes ingresar un teléfono de contacto."
            )

        return telefono


# ============================================================
# FORMULARIOS DE CARACTERÍSTICAS Y ESTANCIAS
# ============================================================

class CaracteristicaCatalogoForm(forms.ModelForm):

    class Meta:
        model = Caracteristica
        fields = ["nombre"]

        labels = {
            "nombre": "Nombre de la característica",
        }

        widgets = {
            "nombre": forms.TextInput(attrs={
                "placeholder": "Ej. Piscina, garaje, terraza",
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()

        if len(nombre) < 2:
            raise forms.ValidationError(
                "El nombre debe tener al menos 2 caracteres."
            )

        return nombre


class EstanciaCatalogoForm(forms.ModelForm):

    class Meta:
        model = Estancia
        fields = ["nombre"]

        labels = {
            "nombre": "Nombre de la estancia",
        }

        widgets = {
            "nombre": forms.TextInput(attrs={
                "placeholder": "Ej. Habitación, baño, cocina",
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()

        if len(nombre) < 2:
            raise forms.ValidationError(
                "El nombre debe tener al menos 2 caracteres."
            )

        return nombre


class AsignarCaracteristicaForm(forms.Form):

    caracteristica = forms.ModelChoiceField(
        queryset=Caracteristica.objects.none(),
        label="Característica",
        empty_label="Selecciona una característica",
    )

    detalle = forms.CharField(
        label="Detalle adicional",
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={
            "placeholder": "Ej. Garaje cubierto para dos vehículos",
        }),
    )

    def __init__(self, *args, inmueble=None, **kwargs):
        super().__init__(*args, **kwargs)

        disponibles = Caracteristica.objects.all()

        if inmueble is not None:
            asignadas = InmuebleCaracteristica.objects.filter(
                id_inmueble_id=inmueble.pk
            ).values_list("id_caracteristica_id", flat=True)

            disponibles = disponibles.exclude(
                pk__in=asignadas
            )

        self.fields["caracteristica"].queryset = (
            disponibles.order_by("nombre")
        )


class EditarCaracteristicaAsignadaForm(forms.Form):

    detalle = forms.CharField(
        label="Detalle adicional",
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={
            "placeholder": "Descripción de la característica",
        }),
    )


class AsignarEstanciaForm(forms.Form):

    estancia = forms.ModelChoiceField(
        queryset=Estancia.objects.none(),
        label="Tipo de estancia",
        empty_label="Selecciona una estancia",
    )

    cantidad = forms.IntegerField(
        label="Cantidad",
        min_value=1,
        widget=forms.NumberInput(attrs={
            "min": "1",
        }),
    )

    def __init__(self, *args, inmueble=None, **kwargs):
        super().__init__(*args, **kwargs)

        disponibles = Estancia.objects.all()

        if inmueble is not None:
            asignadas = ViviendaEstancia.objects.filter(
                id_inmueble_id=inmueble.pk
            ).values_list("id_estancia_id", flat=True)

            disponibles = disponibles.exclude(
                pk__in=asignadas
            )

        self.fields["estancia"].queryset = (
            disponibles.order_by("nombre")
        )


class EditarEstanciaAsignadaForm(forms.Form):

    cantidad = forms.IntegerField(
        label="Cantidad",
        min_value=1,
        widget=forms.NumberInput(attrs={
            "min": "1",
        }),
    )


# ============================================================
# FORMULARIO DE VISITAS
# ============================================================

class VisitaForm(forms.ModelForm):

    class Meta:
        model = Visita

        fields = [
            "id_cliente",
            "id_inmueble",
            "fecha_hora",
            "comentario",
        ]

        labels = {
            "id_cliente": "Cliente",
            "id_inmueble": "Inmueble",
            "fecha_hora": "Fecha y hora de la visita",
            "comentario": "Comentarios",
        }

        widgets = {
            "fecha_hora": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "step": "60",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "comentario": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": (
                    "Observaciones sobre la visita..."
                ),
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["id_cliente"].queryset = (
            Cliente.objects.order_by("nombre")
        )

        self.fields["id_inmueble"].queryset = (
            Inmueble.objects.order_by("referencia")
        )

        self.fields["id_cliente"].label_from_instance = (
            lambda cliente: (
                f"{cliente.nombre} — ID {cliente.pk}"
            )
        )

        self.fields["id_inmueble"].label_from_instance = (
            lambda inmueble: (
                f"{inmueble.referencia} — "
                f"{inmueble.get_tipo_display()} — "
                f"{inmueble.direccion}"
            )
        )

        self.fields["fecha_hora"].input_formats = [
            "%Y-%m-%dT%H:%M",
            "%Y-%m-%d %H:%M:%S",
        ]

        if self.instance and self.instance.pk:
            fecha = self.instance.fecha_hora

            if fecha:
                if timezone.is_aware(fecha):
                    fecha = timezone.localtime(fecha)

                self.initial["fecha_hora"] = fecha.strftime(
                    "%Y-%m-%dT%H:%M"
                )

    def clean_fecha_hora(self):
        fecha = self.cleaned_data["fecha_hora"]
        fecha_original = (
            self.instance.fecha_hora
            if self.instance and self.instance.pk
            else None
        )

        if fecha_original and fecha == fecha_original:
            return fecha

        if fecha < timezone.now():
            raise forms.ValidationError(
                "No puedes programar o reprogramar "
                "una visita en el pasado."
            )

        return fecha


# ============================================================
# GESTIÓN DE CLIENTES
# ============================================================

class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ["nombre", "telefono"]

        labels = {
            "nombre": "Nombre completo",
            "telefono": "Teléfono de contacto",
        }

        widgets = {
            "nombre": forms.TextInput(attrs={
                "placeholder": "Nombre completo del cliente",
                "autocomplete": "name",
            }),
            "telefono": forms.TextInput(attrs={
                "placeholder": "Número de teléfono",
                "autocomplete": "tel",
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()

        if len(nombre) < 3:
            raise forms.ValidationError(
                "El nombre debe tener al menos 3 caracteres."
            )

        return nombre

    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono") or ""
        return telefono.strip()


class VincularUsuarioClienteForm(forms.Form):

    usuario = forms.ModelChoiceField(
        queryset=get_user_model().objects.none(),
        required=False,
        label="Cuenta de usuario",
        empty_label="Sin cuenta vinculada",
    )

    def __init__(self, *args, cliente=None, **kwargs):
        super().__init__(*args, **kwargs)

        Usuario = get_user_model()

        # Solo cuentas del grupo Cliente.
        usuarios = Usuario.objects.filter(
            groups__name="Cliente"
        )

        # Excluir cuentas vinculadas a otros clientes.
        ocupados = Cliente.objects.exclude(
            pk=cliente.pk if cliente else None
        ).exclude(
            usuario_id__isnull=True
        ).values_list("usuario_id", flat=True)

        self.fields["usuario"].queryset = (
            usuarios.exclude(pk__in=ocupados)
            .distinct()
            .order_by("username")
        )

        self.fields["usuario"].label_from_instance = (
            lambda usuario: (
                f"{usuario.username} — {usuario.email}"
            )
        )

        if cliente and cliente.usuario_id:
            self.initial["usuario"] = cliente.usuario_id

