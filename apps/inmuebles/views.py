
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)
from django.views.decorators.http import require_POST

from django.core.exceptions import PermissionDenied, ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError, DatabaseError
from django.db.models import Count, Prefetch, Q
from django.utils import timezone

from apps.cuentas.roles import obtener_rol

from .models import (
    Cliente,
    Inmueble,
    Piso,
    Casa,
    Villa,
    Local,
    Oferta,
    Vivienda,
    ViviendaEstancia,
    InmuebleCaracteristica,
    Propietario,
    Caracteristica,
    Estancia,
    Visita,
)

from .forms import (
    ClienteForm,
    CrearInmuebleForm,
    EditarInmuebleForm,
    OfertaForm,
    PropietarioForm,
    FORMULARIOS_TIPO,
    CaracteristicaCatalogoForm,
    EstanciaCatalogoForm,
    AsignarCaracteristicaForm,
    EditarCaracteristicaAsignadaForm,
    AsignarEstanciaForm,
    EditarEstanciaAsignadaForm,
    VisitaForm,
    VincularUsuarioClienteForm,
)
from .clientes_services import (
    crear_cliente,
    actualizar_cliente,
    vincular_usuario,
    eliminar_cliente,
)
from .services import (
    crear_inmueble,
    actualizar_inmueble,
    eliminar_inmueble,
)
from .ofertas_services import (
    crear_oferta,
    actualizar_oferta,
    eliminar_oferta,
)
from .propietarios_services import (
    crear_propietario,
    actualizar_propietario,
    eliminar_propietario,
)
from .atributos_services import (
    asignar_caracteristica,
    actualizar_caracteristica_asignada,
    quitar_caracteristica,
    asignar_estancia,
    actualizar_estancia_asignada,
    quitar_estancia,
)
from .visitas_services import (
    crear_visita,
    actualizar_visita,
    eliminar_visita,
)


# ============================================================
# 1. CATÁLOGO PÚBLICO DE INMUEBLES
# ============================================================

def preparar_ofertas_inmuebles(inmuebles):
    """
    Adjunta a cada inmueble sus ofertas de venta
    y alquiler, para facilitar su presentación.
    """

    for inmueble in inmuebles:
        ofertas = list(inmueble.ofertas_precargadas)

        inmueble.oferta_venta = next(
            (
                oferta for oferta in ofertas
                if oferta.modalidad == "VENTA"
            ),
            None
        )

        inmueble.oferta_alquiler = next(
            (
                oferta for oferta in ofertas
                if oferta.modalidad == "ALQUILER"
            ),
            None
        )

    return inmuebles


def lista_inmuebles(request):
    inmuebles = list(
        Inmueble.objects
        .prefetch_related(
            Prefetch(
                "oferta_set",
                queryset=Oferta.objects.order_by("modalidad"),
                to_attr="ofertas_precargadas"
            )
        )
        .order_by("referencia")
    )

    preparar_ofertas_inmuebles(inmuebles)

    return render(
        request,
        "inmuebles/lista.html",
        {
            "inmuebles": inmuebles
        }
    )


# ============================================================
# 2. LISTADO ADMINISTRATIVO DE INMUEBLES
# ============================================================

@permission_required(
    "inmuebles.view_inmueble",
    raise_exception=True
)
def gestionar_inmuebles(request):
    """
    Muestra el listado administrativo de inmuebles.

    Solo pueden acceder administradores y vendedores
    con el permiso correspondiente.
    """

    if not (
        request.user.is_superuser
        or request.user.groups.filter(
            name__in=["Administrador", "Vendedor"]
        ).exists()
    ):
        raise PermissionDenied

    busqueda = request.GET.get("q", "").strip()
    tipo = request.GET.get("tipo", "").strip()

    inmuebles = Inmueble.objects.all()

    if busqueda:
        inmuebles = inmuebles.filter(
            Q(referencia__icontains=busqueda)
            | Q(direccion__icontains=busqueda)
        )

    tipos_validos = ["PISO", "CASA", "VILLA", "LOCAL"]

    if tipo in tipos_validos:
        inmuebles = inmuebles.filter(tipo=tipo)
    else:
        tipo = ""

    inmuebles = list(
        inmuebles.prefetch_related(
            Prefetch(
                "oferta_set",
                queryset=Oferta.objects.order_by("modalidad"),
                to_attr="ofertas_precargadas"
            )
        ).order_by("referencia")
    )

    preparar_ofertas_inmuebles(inmuebles)

    return render(
        request,
        "inmuebles/gestion/listar.html",
        {
            "inmuebles": inmuebles,
            "busqueda": busqueda,
            "tipo_seleccionado": tipo,
        }
    )


# ============================================================
# 3. REDIRECCIÓN SEGÚN EL ROL
# ============================================================

def redireccion_inmuebles(request):
    """
    Redirige al usuario según su rol:

    Administrador -> Gestión de inmuebles
    Vendedor      -> Gestión de inmuebles
    Cliente       -> Catálogo público
    Visitante     -> Catálogo público
    """

    rol = obtener_rol(request.user)

    if rol in ["Administrador", "Vendedor"]:
        return redirect("inmuebles:gestionar")

    return redirect("inmuebles:lista")


# ============================================================
# 4. PÁGINA PRINCIPAL
# ============================================================

def inicio(request):
    """
    Muestra la página principal de la inmobiliaria.

    Presenta los últimos tres inmuebles registrados.
    """

    inmuebles_destacados = (
        Inmueble.objects.all()
        .order_by("-id_inmueble")[:3]
    )

    contexto = {
        "inmuebles_destacados": inmuebles_destacados,
    }

    return render(
        request,
        "inmuebles/index.html",
        contexto
    )


# ============================================================
# 5. REGISTRAR UN NUEVO INMUEBLE
# ============================================================

@login_required
@permission_required(
    "inmuebles.add_inmueble",
    raise_exception=True
)
def registrar_inmueble(request):
    """
    Permite registrar inmuebles de tipo:

    - PISO
    - CASA
    - VILLA
    - LOCAL

    Valida los datos generales y específicos
    antes de ejecutar el guardado transaccional.
    """

    # --------------------------------------------------------
    # 1. Verificar que sea personal interno
    # --------------------------------------------------------

    usuario = request.user

    personal_interno = (
        usuario.is_superuser
        or usuario.groups.filter(
            name__in=["Administrador", "Vendedor"]
        ).exists()
    )

    if not personal_interno:
        raise PermissionDenied

    # --------------------------------------------------------
    # 2. Inicializar variables
    # --------------------------------------------------------

    tipo_seleccionado = ""
    formulario_especifico = None

    # --------------------------------------------------------
    # 3. Procesar el formulario enviado
    # --------------------------------------------------------

    if request.method == "POST":

        formulario = CrearInmuebleForm(request.POST)

        tipo_seleccionado = request.POST.get(
            "tipo", ""
        )

        clase_formulario = FORMULARIOS_TIPO.get(
            tipo_seleccionado
        )

        # Crear formulario específico según el tipo.
        if clase_formulario is not None:

            formulario_especifico = clase_formulario(
                request.POST,
                prefix="especifico"
            )

        # ----------------------------------------------------
        # 4. Validar ambos formularios
        # ----------------------------------------------------

        formulario_valido = formulario.is_valid()

        especifico_valido = (
            formulario_especifico is not None
            and formulario_especifico.is_valid()
        )

        # ----------------------------------------------------
        # 5. Guardar si todos los datos son válidos
        # ----------------------------------------------------

        if formulario_valido and especifico_valido:

            try:

                inmueble = crear_inmueble(
                    formulario,
                    formulario_especifico.cleaned_data
                )

            except IntegrityError:

                messages.error(
                    request,
                    "No fue posible registrar el inmueble. "
                    "Verifica que los datos no estén "
                    "duplicados y que las relaciones "
                    "sean válidas."
                )

            else:

                messages.success(
                    request,
                    f"El inmueble {inmueble.referencia} "
                    "se registró correctamente."
                )

                return redirect(
                    "inmuebles:gestionar"
                )

    # --------------------------------------------------------
    # 6. Mostrar formulario vacío (GET)
    # --------------------------------------------------------

    else:

        formulario = CrearInmuebleForm()

    # --------------------------------------------------------
    # 7. Preparar formularios para la plantilla
    # --------------------------------------------------------

    formularios_tipos = {}

    for tipo, clase in FORMULARIOS_TIPO.items():

        # Mantener los datos y errores del formulario
        # específico que el usuario estaba completando.
        if (
            request.method == "POST"
            and tipo == tipo_seleccionado
            and formulario_especifico is not None
        ):

            formularios_tipos[tipo] = formulario_especifico

        else:

            formularios_tipos[tipo] = clase(
                prefix="especifico"
            )

    # --------------------------------------------------------
    # 8. Renderizar la página
    # --------------------------------------------------------

    contexto = {
        "formulario": formulario,
        "formularios_tipos": formularios_tipos,
        "tipo_seleccionado": tipo_seleccionado,
    }

    return render(
        request,
        "inmuebles/gestion/crear.html",
        contexto
    )


# ============================================================
# 6. EDITAR UN INMUEBLE EXISTENTE
# ============================================================

@login_required
@permission_required(
    "inmuebles.change_inmueble",
    raise_exception=True
)
def editar_inmueble(request, inmueble_id):
    """
    Edita los datos generales y específicos de
    un inmueble, sin permitir cambiar su tipo.
    """

    usuario = request.user

    personal_interno = (
        usuario.is_superuser
        or usuario.groups.filter(
            name__in=["Administrador", "Vendedor"]
        ).exists()
    )

    if not personal_interno:
        raise PermissionDenied

    inmueble = get_object_or_404(
        Inmueble,
        pk=inmueble_id
    )

    tipo = inmueble.tipo

    clase_formulario = FORMULARIOS_TIPO.get(tipo)

    if clase_formulario is None:
        raise ValidationError(
            "El inmueble tiene un tipo no válido."
        )

    # --------------------------------------------------------
    # 1. Obtener los datos específicos existentes
    # --------------------------------------------------------

    try:
        if tipo == "PISO":

            especializacion = Piso.objects.get(
                id_inmueble_id=inmueble.pk,
                tipo="PISO"
            )

            datos_iniciales = {
                "estado": especializacion.estado
            }

        elif tipo == "CASA":

            Casa.objects.get(
                id_inmueble_id=inmueble.pk,
                tipo="CASA"
            )

            datos_iniciales = {}

        elif tipo == "VILLA":

            especializacion = Villa.objects.get(
                id_inmueble_id=inmueble.pk,
                tipo="VILLA"
            )

            datos_iniciales = {
                "superficie_parcela_m2": (
                    especializacion.superficie_parcela_m2
                ),
                "urbanizacion": especializacion.urbanizacion,
            }

        else:

            especializacion = Local.objects.get(
                id_inmueble_id=inmueble.pk,
                tipo="LOCAL"
            )

            datos_iniciales = {
                "numero_puertas": especializacion.numero_puertas,
                "es_diafano": (
                    ""
                    if especializacion.es_diafano is None
                    else "1" if especializacion.es_diafano else "0"
                ),
                "esta_acondicionado": (
                    ""
                    if especializacion.esta_acondicionado is None
                    else "1" if especializacion.esta_acondicionado else "0"
                ),
            }

    except (
        Piso.DoesNotExist,
        Casa.DoesNotExist,
        Villa.DoesNotExist,
        Local.DoesNotExist,
    ):
        messages.error(
            request,
            "Este inmueble no tiene una especialización "
            "válida. Revisa sus registros relacionados."
        )

        return redirect("inmuebles:gestionar")

    # --------------------------------------------------------
    # 2. Procesar formulario
    # --------------------------------------------------------

    if request.method == "POST":

        formulario = EditarInmuebleForm(
            request.POST,
            instance=inmueble
        )

        formulario_especifico = clase_formulario(
            request.POST,
            prefix="especifico"
        )

        general_valido = formulario.is_valid()
        especifico_valido = formulario_especifico.is_valid()

        if general_valido and especifico_valido:

            try:

                inmueble_actualizado = actualizar_inmueble(
                    inmueble.pk,
                    formulario,
                    formulario_especifico.cleaned_data
                )

            except (IntegrityError, DatabaseError, ValidationError):

                messages.error(
                    request,
                    "No fue posible actualizar el inmueble. "
                    "Verifica sus datos e inténtalo nuevamente."
                )

            else:

                messages.success(
                    request,
                    f"El inmueble "
                    f"{inmueble_actualizado.referencia} "
                    "se actualizó correctamente."
                )

                return redirect("inmuebles:gestionar")

    else:

        formulario = EditarInmuebleForm(
            instance=inmueble
        )

        formulario_especifico = clase_formulario(
            initial=datos_iniciales,
            prefix="especifico"
        )

    # --------------------------------------------------------
    # 3. Renderizar
    # --------------------------------------------------------

    contexto = {
        "inmueble": inmueble,
        "formulario": formulario,
        "formulario_especifico": formulario_especifico,
    }

    return render(
        request,
        "inmuebles/gestion/editar.html",
        contexto
    )


# ============================================================
# 7. ELIMINAR UN INMUEBLE
# ============================================================

@login_required
@permission_required(
    "inmuebles.delete_inmueble",
    raise_exception=True
)
@require_POST
def borrar_inmueble(request, inmueble_id):
    """
    Elimina un inmueble mediante POST.

    Solo el personal autorizado puede ejecutar
    esta operación.
    """

    usuario = request.user

    # Comprobar rol interno.
    personal_interno = (
        usuario.is_superuser
        or usuario.groups.filter(
            name="Administrador"
        ).exists()
    )

    if not personal_interno:
        raise PermissionDenied

    try:

        referencia = eliminar_inmueble(
            inmueble_id
        )

    except Inmueble.DoesNotExist:

        messages.error(
            request,
            "El inmueble que intentas eliminar "
            "ya no existe."
        )

    except ValidationError as error:

        messages.error(
            request,
            " ".join(error.messages)
        )

    except (IntegrityError, DatabaseError):

        messages.error(
            request,
            "No fue posible eliminar el inmueble "
            "porque existen restricciones o "
            "registros relacionados que impiden "
            "la operación."
        )

    else:

        messages.success(
            request,
            f"El inmueble {referencia} "
            "se eliminó correctamente."
        )

    return redirect(
        "inmuebles:gestionar"
    )


# ============================================================
# GESTIÓN DE OFERTAS COMERCIALES
# ============================================================

def verificar_personal_interno(usuario):
    """
    Verifica que el usuario pertenezca al personal
    autorizado de la inmobiliaria.
    """

    if not (
        usuario.is_superuser
        or usuario.groups.filter(
            name__in=["Administrador", "Vendedor"]
        ).exists()
    ):
        raise PermissionDenied


# ============================================================
# 1. LISTAR OFERTAS DE UN INMUEBLE
# ============================================================

@login_required
@permission_required(
    "inmuebles.view_inmueble",
    raise_exception=True
)
def listar_ofertas(request, inmueble_id):

    verificar_personal_interno(request.user)

    inmueble = get_object_or_404(
        Inmueble,
        pk=inmueble_id
    )

    ofertas = Oferta.objects.filter(
        id_inmueble=inmueble
    ).order_by("modalidad")

    modalidades_existentes = set(
        ofertas.values_list("modalidad", flat=True)
    )

    contexto = {
        "inmueble": inmueble,
        "ofertas": ofertas,
        "puede_crear": (
            request.user.has_perm(
                "inmuebles.add_inmueble"
            )
            and len(modalidades_existentes) < 2
        ),
    }

    return render(
        request,
        "inmuebles/ofertas/listar.html",
        contexto
    )


# ============================================================
# 2. CREAR OFERTA
# ============================================================

@login_required
@permission_required(
    "inmuebles.add_inmueble",
    raise_exception=True
)
def registrar_oferta(request, inmueble_id):

    verificar_personal_interno(request.user)

    inmueble = get_object_or_404(
        Inmueble,
        pk=inmueble_id
    )

    if request.method == "POST":

        formulario = OfertaForm(
            request.POST,
            inmueble=inmueble
        )

        if formulario.is_valid():

            try:
                oferta = crear_oferta(
                    inmueble.pk,
                    formulario
                )

            except ValidationError as error:
                formulario.add_error(
                    None,
                    " ".join(error.messages)
                )

            except (IntegrityError, DatabaseError):
                formulario.add_error(
                    None,
                    "No fue posible registrar la oferta. "
                    "Comprueba que no exista otra oferta "
                    "de la misma modalidad."
                )

            else:
                messages.success(
                    request,
                    f"Oferta de {oferta.get_modalidad_display()} "
                    "registrada correctamente."
                )

                return redirect(
                    "inmuebles:ofertas",
                    inmueble_id=inmueble.pk
                )

    else:
        formulario = OfertaForm(
            inmueble=inmueble
        )

    return render(
        request,
        "inmuebles/ofertas/formulario.html",
        {
            "inmueble": inmueble,
            "formulario": formulario,
            "modo": "crear",
        }
    )


# ============================================================
# 3. EDITAR OFERTA
# ============================================================

@login_required
@permission_required(
    "inmuebles.change_inmueble",
    raise_exception=True
)
def editar_oferta(request, oferta_id):

    verificar_personal_interno(request.user)

    oferta = get_object_or_404(
        Oferta.objects.select_related("id_inmueble"),
        pk=oferta_id
    )

    inmueble = oferta.id_inmueble

    if request.method == "POST":

        formulario = OfertaForm(
            request.POST,
            instance=oferta,
            inmueble=inmueble
        )

        if formulario.is_valid():

            try:
                oferta_actualizada = actualizar_oferta(
                    oferta.pk,
                    formulario
                )

            except (IntegrityError, DatabaseError):
                formulario.add_error(
                    None,
                    "No fue posible actualizar la oferta."
                )

            else:
                messages.success(
                    request,
                    "Oferta comercial actualizada "
                    "correctamente."
                )

                return redirect(
                    "inmuebles:ofertas",
                    inmueble_id=oferta_actualizada.id_inmueble_id
                )

    else:
        formulario = OfertaForm(
            instance=oferta,
            inmueble=inmueble
        )

    return render(
        request,
        "inmuebles/ofertas/formulario.html",
        {
            "inmueble": inmueble,
            "formulario": formulario,
            "modo": "editar",
        }
    )


# ============================================================
# 4. ELIMINAR OFERTA
# ============================================================


@login_required
@permission_required(
    "inmuebles.change_inmueble",
    raise_exception=True
)
@require_POST
def borrar_oferta(request, oferta_id):

    verificar_personal_interno(request.user)

    oferta = get_object_or_404(
        Oferta,
        pk=oferta_id
    )

    inmueble_id = oferta.id_inmueble_id

    try:
        eliminar_oferta(oferta.pk)

    except Oferta.DoesNotExist:
        messages.error(
            request,
            "La oferta ya no existe."
        )

    except (IntegrityError, DatabaseError):
        messages.error(
            request,
            "No fue posible eliminar la oferta."
        )

    else:
        messages.success(
            request,
            "La oferta comercial fue eliminada."
        )

    return redirect(
        "inmuebles:ofertas",
        inmueble_id=inmueble_id
    )


# ============================================================
# DETALLE PÚBLICO Y ADMINISTRATIVO DE UN INMUEBLE
# ============================================================

def detalle_inmueble(request, inmueble_id):

    inmueble = get_object_or_404(
        Inmueble.objects.select_related(
            "id_propietario",
            "id_oficina_gestion",
            "id_oficina_llaves",
            "id_zona",
        ).prefetch_related(
            Prefetch(
                "oferta_set",
                queryset=Oferta.objects.order_by("modalidad"),
                to_attr="ofertas_precargadas"
            )
        ),
        pk=inmueble_id
    )

    preparar_ofertas_inmuebles([inmueble])

    # --------------------------------------------------------
    # 1. Determinar permisos
    # --------------------------------------------------------

    usuario = request.user

    personal_interno = (
        usuario.is_authenticated
        and (
            usuario.is_superuser
            or usuario.groups.filter(
                name__in=["Administrador", "Vendedor"]
            ).exists()
        )
    )

    administrador = (
        usuario.is_authenticated
        and (
            usuario.is_superuser
            or usuario.groups.filter(
                name="Administrador"
            ).exists()
        )
    )

    puede_editar = (
        personal_interno
        and usuario.has_perm("inmuebles.change_inmueble")
    )

    puede_crear_oferta = (
        personal_interno
        and usuario.has_perm("inmuebles.add_inmueble")
    )

    puede_eliminar = (
        administrador
        and usuario.has_perm("inmuebles.delete_inmueble")
    )

    # --------------------------------------------------------
    # 2. Recuperar información específica
    # --------------------------------------------------------

    datos_especificos = []

    if inmueble.tipo == "PISO":

        piso = Piso.objects.filter(
            id_inmueble_id=inmueble.pk
        ).first()

        if piso:
            datos_especificos.append(
                ("Estado", piso.get_estado_display())
            )

    elif inmueble.tipo == "CASA":

        # La tabla casa no tiene atributos adicionales.
        pass

    elif inmueble.tipo == "VILLA":

        villa = Villa.objects.filter(
            id_inmueble_id=inmueble.pk
        ).first()

        if villa:
            datos_especificos.extend([
                (
                    "Superficie de parcela",
                    f"{villa.superficie_parcela_m2} m²"
                ),
                (
                    "Urbanización",
                    villa.urbanizacion
                ),
            ])

    elif inmueble.tipo == "LOCAL":

        local = Local.objects.filter(
            id_inmueble_id=inmueble.pk
        ).first()

        if local:

            def mostrar_booleano(valor):
                if valor is None:
                    return "Sin especificar"
                return "Sí" if valor else "No"

            datos_especificos.extend([
                (
                    "Número de puertas",
                    local.numero_puertas
                    if local.numero_puertas is not None
                    else "Sin especificar"
                ),
                (
                    "Diáfano",
                    mostrar_booleano(local.es_diafano)
                ),
                (
                    "Acondicionado",
                    mostrar_booleano(local.esta_acondicionado)
                ),
            ])

    # --------------------------------------------------------
    # 3. Características registradas
    # --------------------------------------------------------

    caracteristicas = (
        InmuebleCaracteristica.objects
        .filter(id_inmueble_id=inmueble.pk)
        .select_related("id_caracteristica")
        .order_by("id_caracteristica__nombre")
    )

    # --------------------------------------------------------
    # 4. Estancias de las viviendas
    # --------------------------------------------------------

    estancias = []

    if inmueble.tipo in ("PISO", "CASA", "VILLA"):

        estancias = (
            ViviendaEstancia.objects
            .filter(id_inmueble_id=inmueble.pk)
            .select_related("id_estancia")
            .order_by("id_estancia__nombre")
        )

    # --------------------------------------------------------
    # 5. Renderizar
    # --------------------------------------------------------

    return render(
        request,
        "inmuebles/detalle.html",
        {
            "inmueble": inmueble,
            "datos_especificos": datos_especificos,
            "caracteristicas": caracteristicas,
            "estancias": estancias,
            "personal_interno": personal_interno,
            "puede_editar": puede_editar,
            "puede_crear_oferta": puede_crear_oferta,
            "puede_eliminar": puede_eliminar,
        }
    )


# ============================================================
# GESTIÓN DE PROPIETARIOS
# ============================================================


# ============================================================
# 1. LISTAR PROPIETARIOS
# ============================================================

@login_required
@permission_required(
    "inmuebles.view_inmueble",
    raise_exception=True
)
def listar_propietarios(request):

    verificar_personal_interno(request.user)

    administrador = (
        request.user.is_superuser
        or request.user.groups.filter(
            name="Administrador"
        ).exists()
    )
    puede_eliminar_propietarios = (
        administrador
        and request.user.has_perm(
            "inmuebles.delete_inmueble"
        )
    )

    busqueda = request.GET.get("q", "").strip()

    propietarios = Propietario.objects.all()

    if busqueda:
        propietarios = propietarios.filter(
            Q(nombre__icontains=busqueda)
            | Q(telefono__icontains=busqueda)
        )

    propietarios = propietarios.order_by(
        "nombre",
        "id_propietario"
    )

    # Número de inmuebles asociados a cada propietario.
    from django.db.models import Count

    propietarios = propietarios.annotate(
        total_inmuebles=Count("inmueble")
    )

    paginador = Paginator(propietarios, 10)
    pagina = paginador.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "inmuebles/propietarios/listar.html",
        {
            "propietarios": pagina,
            "busqueda": busqueda,
            "puede_eliminar_propietarios": puede_eliminar_propietarios,
        }
    )


# ============================================================
# 2. DETALLE DE PROPIETARIO
# ============================================================

@login_required
@permission_required(
    "inmuebles.view_inmueble",
    raise_exception=True
)
def detalle_propietario(request, propietario_id):

    verificar_personal_interno(request.user)

    propietario = get_object_or_404(
        Propietario,
        pk=propietario_id
    )

    inmuebles = (
        Inmueble.objects
        .filter(id_propietario=propietario)
        .order_by("referencia")
    )

    administrador = (
        request.user.is_superuser
        or request.user.groups.filter(
            name="Administrador"
        ).exists()
    )

    return render(
        request,
        "inmuebles/propietarios/detalle.html",
        {
            "propietario": propietario,
            "inmuebles": inmuebles,
            "puede_editar": request.user.has_perm(
                "inmuebles.change_inmueble"
            ),
            "puede_eliminar": (
                administrador
                and request.user.has_perm(
                    "inmuebles.delete_inmueble"
                )
                and not inmuebles.exists()
            ),
        }
    )


# ============================================================
# 3. CREAR PROPIETARIO
# ============================================================

@login_required
@permission_required(
    "inmuebles.add_inmueble",
    raise_exception=True
)
def registrar_propietario(request):

    verificar_personal_interno(request.user)

    if request.method == "POST":

        formulario = PropietarioForm(request.POST)

        if formulario.is_valid():

            try:
                propietario = crear_propietario(
                    formulario
                )

            except (IntegrityError, DatabaseError):
                formulario.add_error(
                    None,
                    "No fue posible registrar el propietario."
                )

            else:
                messages.success(
                    request,
                    f"El propietario {propietario.nombre} "
                    "se registró correctamente."
                )

                return redirect(
                    "inmuebles:propietarios"
                )

    else:
        formulario = PropietarioForm()

    return render(
        request,
        "inmuebles/propietarios/formulario.html",
        {
            "formulario": formulario,
            "modo": "crear",
        }
    )


# ============================================================
# 4. EDITAR PROPIETARIO
# ============================================================

@login_required
@permission_required(
    "inmuebles.change_inmueble",
    raise_exception=True
)
def editar_propietario(request, propietario_id):

    verificar_personal_interno(request.user)

    propietario = get_object_or_404(
        Propietario,
        pk=propietario_id
    )

    if request.method == "POST":

        formulario = PropietarioForm(
            request.POST,
            instance=propietario
        )

        if formulario.is_valid():

            try:
                propietario_actualizado = (
                    actualizar_propietario(
                        propietario.pk,
                        formulario
                    )
                )

            except (IntegrityError, DatabaseError):
                formulario.add_error(
                    None,
                    "No fue posible actualizar el propietario."
                )

            else:
                messages.success(
                    request,
                    "Los datos del propietario "
                    "se actualizaron correctamente."
                )

                return redirect(
                    "inmuebles:detalle_propietario",
                    propietario_id=propietario_actualizado.pk
                )

    else:
        formulario = PropietarioForm(
            instance=propietario
        )

    return render(
        request,
        "inmuebles/propietarios/formulario.html",
        {
            "formulario": formulario,
            "propietario": propietario,
            "modo": "editar",
        }
    )


# ============================================================
# 5. ELIMINAR PROPIETARIO
# ============================================================

@login_required
@permission_required(
    "inmuebles.delete_inmueble",
    raise_exception=True
)
@require_POST
def borrar_propietario(request, propietario_id):

    administrador = (
        request.user.is_superuser
        or request.user.groups.filter(
            name="Administrador"
        ).exists()
    )

    if not administrador:
        raise PermissionDenied

    try:
        nombre = eliminar_propietario(
            propietario_id
        )

    except Propietario.DoesNotExist:
        messages.error(
            request,
            "El propietario ya no existe."
        )

    except ValidationError as error:
        messages.error(
            request,
            " ".join(error.messages)
        )

    except (IntegrityError, DatabaseError):
        messages.error(
            request,
            "No fue posible eliminar el propietario. "
            "Verifica que no tenga registros asociados."
        )

    else:
        messages.success(
            request,
            f"El propietario {nombre} fue eliminado."
        )

    return redirect(
        "inmuebles:propietarios"
    )


# ============================================================
# GESTIÓN DE CARACTERÍSTICAS Y ESTANCIAS
# ============================================================

@login_required
@permission_required(
    "inmuebles.change_inmueble",
    raise_exception=True
)
def gestionar_atributos(request, inmueble_id):

    verificar_personal_interno(request.user)

    inmueble = get_object_or_404(
        Inmueble,
        pk=inmueble_id
    )

    caracteristicas = (
        InmuebleCaracteristica.objects
        .filter(id_inmueble_id=inmueble.pk)
        .select_related("id_caracteristica")
        .order_by("id_caracteristica__nombre")
    )

    estancias = []

    es_vivienda = inmueble.tipo in (
        "PISO", "CASA", "VILLA"
    )

    if es_vivienda:
        estancias = (
            ViviendaEstancia.objects
            .filter(id_inmueble_id=inmueble.pk)
            .select_related("id_estancia")
            .order_by("id_estancia__nombre")
        )

    formulario_caracteristica = (
        AsignarCaracteristicaForm(inmueble=inmueble)
    )

    formulario_estancia = (
        AsignarEstanciaForm(inmueble=inmueble)
        if es_vivienda
        else None
    )

    return render(
        request,
        "inmuebles/atributos/gestionar.html",
        {
            "inmueble": inmueble,
            "caracteristicas": caracteristicas,
            "estancias": estancias,
            "es_vivienda": es_vivienda,
            "formulario_caracteristica": formulario_caracteristica,
            "formulario_estancia": formulario_estancia,
            "puede_administrar_catalogos": (
                request.user.is_superuser
                or request.user.groups.filter(
                    name="Administrador"
                ).exists()
            ),
        }
    )


@login_required
@permission_required(
    "inmuebles.change_inmueble",
    raise_exception=True
)
@require_POST
def agregar_caracteristica(request, inmueble_id):

    verificar_personal_interno(request.user)

    inmueble = get_object_or_404(
        Inmueble,
        pk=inmueble_id
    )

    formulario = AsignarCaracteristicaForm(
        request.POST,
        inmueble=inmueble
    )

    if formulario.is_valid():

        try:
            asignar_caracteristica(
                inmueble.pk,
                formulario.cleaned_data["caracteristica"].pk,
                formulario.cleaned_data["detalle"],
            )

        except (ValidationError, IntegrityError, DatabaseError):
            messages.error(
                request,
                "No fue posible asignar la característica. "
                "Comprueba que no esté repetida."
            )

        else:
            messages.success(
                request,
                "Característica agregada correctamente."
            )

    else:
        messages.error(
            request,
            "Selecciona una característica válida "
            "y revisa el detalle."
        )

    return redirect(
        "inmuebles:gestionar_atributos",
        inmueble_id=inmueble.pk
    )


@login_required
@permission_required(
    "inmuebles.change_inmueble",
    raise_exception=True
)
@require_POST
def modificar_caracteristica(
    request,
    inmueble_id,
    caracteristica_id,
):
    verificar_personal_interno(request.user)

    inmueble = get_object_or_404(
        Inmueble,
        pk=inmueble_id
    )

    formulario = EditarCaracteristicaAsignadaForm(
        request.POST
    )

    if formulario.is_valid():
        try:
            actualizar_caracteristica_asignada(
                inmueble.pk,
                caracteristica_id,
                formulario.cleaned_data["detalle"],
            )
        except (
            InmuebleCaracteristica.DoesNotExist,
            ValidationError,
            IntegrityError,
            DatabaseError,
        ):
            messages.error(
                request,
                "No fue posible actualizar la característica."
            )
        else:
            messages.success(
                request,
                "Característica actualizada."
            )
    else:
        messages.error(
            request,
            "El detalle de la característica no es válido."
        )

    return redirect(
        "inmuebles:gestionar_atributos",
        inmueble_id=inmueble.pk
    )


@login_required
@permission_required(
    "inmuebles.change_inmueble",
    raise_exception=True
)
@require_POST
def eliminar_caracteristica_asignada(
    request,
    inmueble_id,
    caracteristica_id,
):
    verificar_personal_interno(request.user)

    inmueble = get_object_or_404(
        Inmueble,
        pk=inmueble_id
    )

    try:
        quitar_caracteristica(
            inmueble.pk,
            caracteristica_id
        )
    except (ValidationError, IntegrityError, DatabaseError):
        messages.error(
            request,
            "No fue posible quitar la característica."
        )
    else:
        messages.success(
            request,
            "Característica retirada del inmueble."
        )

    return redirect(
        "inmuebles:gestionar_atributos",
        inmueble_id=inmueble.pk
    )


@login_required
@permission_required(
    "inmuebles.change_inmueble",
    raise_exception=True
)
@require_POST
def agregar_estancia(request, inmueble_id):

    verificar_personal_interno(request.user)

    inmueble = get_object_or_404(
        Inmueble,
        pk=inmueble_id
    )

    if inmueble.tipo == "LOCAL":
        raise PermissionDenied(
            "Los locales no admiten estancias."
        )

    formulario = AsignarEstanciaForm(
        request.POST,
        inmueble=inmueble
    )

    if formulario.is_valid():
        try:
            asignar_estancia(
                inmueble.pk,
                formulario.cleaned_data["estancia"].pk,
                formulario.cleaned_data["cantidad"],
            )
        except (
            Vivienda.DoesNotExist,
            ValidationError,
            IntegrityError,
            DatabaseError,
        ):
            messages.error(
                request,
                "No fue posible registrar la estancia."
            )
        else:
            messages.success(
                request,
                "Estancia registrada correctamente."
            )
    else:
        messages.error(
            request,
            "Selecciona una estancia válida y una cantidad "
            "mayor que cero."
        )

    return redirect(
        "inmuebles:gestionar_atributos",
        inmueble_id=inmueble.pk
    )


@login_required
@permission_required(
    "inmuebles.change_inmueble",
    raise_exception=True
)
@require_POST
def modificar_estancia(
    request,
    inmueble_id,
    estancia_id,
):
    verificar_personal_interno(request.user)

    inmueble = get_object_or_404(
        Inmueble,
        pk=inmueble_id
    )

    formulario = EditarEstanciaAsignadaForm(
        request.POST
    )

    if formulario.is_valid():
        try:
            actualizar_estancia_asignada(
                inmueble.pk,
                estancia_id,
                formulario.cleaned_data["cantidad"],
            )
        except (
            ViviendaEstancia.DoesNotExist,
            ValidationError,
            IntegrityError,
            DatabaseError,
        ):
            messages.error(
                request,
                "No fue posible actualizar la estancia."
            )
        else:
            messages.success(
                request,
                "Cantidad de estancias actualizada."
            )
    else:
        messages.error(
            request,
            "La cantidad debe ser mayor que cero."
        )

    return redirect(
        "inmuebles:gestionar_atributos",
        inmueble_id=inmueble.pk
    )


@login_required
@permission_required(
    "inmuebles.change_inmueble",
    raise_exception=True
)
@require_POST
def eliminar_estancia_asignada(
    request,
    inmueble_id,
    estancia_id,
):
    verificar_personal_interno(request.user)

    inmueble = get_object_or_404(
        Inmueble,
        pk=inmueble_id
    )

    try:
        quitar_estancia(
            inmueble.pk,
            estancia_id
        )
    except (ValidationError, IntegrityError, DatabaseError):
        messages.error(
            request,
            "No fue posible quitar la estancia."
        )
    else:
        messages.success(
            request,
            "Estancia retirada de la vivienda."
        )

    return redirect(
        "inmuebles:gestionar_atributos",
        inmueble_id=inmueble.pk
    )


# ============================================================
# CATÁLOGOS DE CARACTERÍSTICAS Y ESTANCIAS
# ============================================================

def verificar_administrador_atributos(usuario):

    if not (
        usuario.is_superuser
        or usuario.groups.filter(
            name="Administrador"
        ).exists()
    ):
        raise PermissionDenied


@login_required
@permission_required(
    "inmuebles.change_inmueble",
    raise_exception=True
)
def catalogos_atributos(request):

    verificar_administrador_atributos(request.user)

    return render(
        request,
        "inmuebles/atributos/catalogos.html",
        {
            "caracteristicas": Caracteristica.objects.order_by(
                "nombre"
            ),
            "estancias": Estancia.objects.order_by(
                "nombre"
            ),
            "formulario_caracteristica": (
                CaracteristicaCatalogoForm()
            ),
            "formulario_estancia": (
                EstanciaCatalogoForm()
            ),
        }
    )


@login_required
@permission_required(
    "inmuebles.change_inmueble",
    raise_exception=True
)
@require_POST
def crear_caracteristica_catalogo(request):

    verificar_administrador_atributos(request.user)

    formulario = CaracteristicaCatalogoForm(request.POST)

    if formulario.is_valid():
        try:
            formulario.save()
        except (IntegrityError, DatabaseError):
            messages.error(
                request,
                "No fue posible crear la característica."
            )
        else:
            messages.success(
                request,
                "Característica creada correctamente."
            )
    else:
        messages.error(
            request,
            "No se pudo registrar la característica. "
            "Comprueba que el nombre sea válido y no exista."
        )

    return redirect("inmuebles:catalogos_atributos")


@login_required
@permission_required(
    "inmuebles.change_inmueble",
    raise_exception=True
)
@require_POST
def crear_estancia_catalogo(request):

    verificar_administrador_atributos(request.user)

    formulario = EstanciaCatalogoForm(request.POST)

    if formulario.is_valid():
        try:
            formulario.save()
        except (IntegrityError, DatabaseError):
            messages.error(
                request,
                "No fue posible crear la estancia."
            )
        else:
            messages.success(
                request,
                "Estancia creada correctamente."
            )
    else:
        messages.error(
            request,
            "No se pudo registrar la estancia. "
            "Comprueba que el nombre sea válido y no exista."
        )

    return redirect("inmuebles:catalogos_atributos")


# ============================================================
# GESTIÓN DE VISITAS
# ============================================================

def verificar_administrador_visitas(usuario):
    if not (
        usuario.is_superuser
        or usuario.groups.filter(
            name="Administrador"
        ).exists()
    ):
        raise PermissionDenied


@login_required
@permission_required(
    "inmuebles.view_inmueble",
    raise_exception=True
)
def listar_visitas(request):

    verificar_personal_interno(request.user)

    busqueda = request.GET.get("q", "").strip()
    filtro = request.GET.get("estado", "todas")

    visitas = (
        Visita.objects
        .select_related("id_cliente", "id_inmueble")
    )

    if busqueda:
        visitas = visitas.filter(
            Q(id_cliente__nombre__icontains=busqueda)
            | Q(id_inmueble__referencia__icontains=busqueda)
            | Q(id_inmueble__direccion__icontains=busqueda)
        )

    ahora = timezone.now()

    if filtro == "proximas":
        visitas = visitas.filter(
            fecha_hora__gte=ahora
        )
    elif filtro == "pasadas":
        visitas = visitas.filter(
            fecha_hora__lt=ahora
        )
    else:
        filtro = "todas"

    visitas = visitas.order_by(
        "-fecha_hora",
        "-id_visita"
    )

    from django.core.paginator import Paginator

    pagina = Paginator(visitas, 10).get_page(
        request.GET.get("page")
    )

    administrador = (
        request.user.is_superuser
        or request.user.groups.filter(
            name="Administrador"
        ).exists()
    )

    return render(
        request,
        "inmuebles/visitas/listar.html",
        {
            "visitas": pagina,
            "busqueda": busqueda,
            "filtro": filtro,
            "puede_eliminar": (
                administrador
                and request.user.has_perm(
                    "inmuebles.delete_inmueble"
                )
            ),
        }
    )


@login_required
@permission_required(
    "inmuebles.add_inmueble",
    raise_exception=True
)
def registrar_visita(request):

    verificar_personal_interno(request.user)

    inmueble_inicial = request.GET.get("inmueble")

    if request.method == "POST":
        formulario = VisitaForm(request.POST)
    else:
        initial = {}

        if inmueble_inicial:
            inmueble = get_object_or_404(
                Inmueble,
                pk=inmueble_inicial
            )
            initial["id_inmueble"] = inmueble.pk

        formulario = VisitaForm(initial=initial)

    if request.method == "POST" and formulario.is_valid():
        try:
            visita = crear_visita(formulario)

        except (IntegrityError, DatabaseError):
            formulario.add_error(
                None,
                "No fue posible registrar la visita."
            )

        else:
            messages.success(
                request,
                "La visita se programó correctamente."
            )

            return redirect(
                "inmuebles:detalle_visita",
                visita_id=visita.pk
            )

    return render(
        request,
        "inmuebles/visitas/formulario.html",
        {
            "formulario": formulario,
            "modo": "crear",
        }
    )


@login_required
@permission_required(
    "inmuebles.view_inmueble",
    raise_exception=True
)
def detalle_visita(request, visita_id):

    verificar_personal_interno(request.user)

    visita = get_object_or_404(
        Visita.objects.select_related(
            "id_cliente",
            "id_inmueble"
        ),
        pk=visita_id
    )

    administrador = (
        request.user.is_superuser
        or request.user.groups.filter(
            name="Administrador"
        ).exists()
    )

    return render(
        request,
        "inmuebles/visitas/detalle.html",
        {
            "visita": visita,
            "puede_editar": request.user.has_perm(
                "inmuebles.change_inmueble"
            ),
            "puede_eliminar": (
                administrador
                and request.user.has_perm(
                    "inmuebles.delete_inmueble"
                )
            ),
        }
    )


@login_required
@permission_required(
    "inmuebles.change_inmueble",
    raise_exception=True
)
def editar_visita(request, visita_id):

    verificar_personal_interno(request.user)

    visita = get_object_or_404(
        Visita,
        pk=visita_id
    )

    if request.method == "POST":
        formulario = VisitaForm(
            request.POST,
            instance=visita
        )
    else:
        formulario = VisitaForm(instance=visita)

    if request.method == "POST" and formulario.is_valid():
        try:
            actualizar_visita(
                visita.pk,
                formulario
            )

        except (IntegrityError, DatabaseError):
            formulario.add_error(
                None,
                "No fue posible actualizar la visita."
            )

        else:
            messages.success(
                request,
                "La visita se actualizó correctamente."
            )

            return redirect(
                "inmuebles:detalle_visita",
                visita_id=visita.pk
            )

    return render(
        request,
        "inmuebles/visitas/formulario.html",
        {
            "formulario": formulario,
            "modo": "editar",
            "visita": visita,
        }
    )


@login_required
@permission_required(
    "inmuebles.delete_inmueble",
    raise_exception=True
)
@require_POST
def borrar_visita(request, visita_id):

    verificar_administrador_visitas(request.user)

    try:
        eliminar_visita(visita_id)

    except Visita.DoesNotExist:
        messages.error(
            request,
            "La visita ya no existe."
        )

    except (IntegrityError, DatabaseError):
        messages.error(
            request,
            "No fue posible eliminar la visita."
        )

    else:
        messages.success(
            request,
            "La visita fue eliminada correctamente."
        )

    return redirect("inmuebles:visitas")


# ============================================================
# MÓDULO DE CLIENTES
# ============================================================

def es_administrador_clientes(usuario):
    return (
        usuario.is_superuser
        or usuario.groups.filter(
            name="Administrador"
        ).exists()
    )


@login_required
@permission_required(
    "inmuebles.view_inmueble",
    raise_exception=True
)
def listar_clientes(request):

    verificar_personal_interno(request.user)

    busqueda = request.GET.get("q", "").strip()

    clientes = (
        Cliente.objects
        .select_related("usuario")
        .annotate(
            total_visitas=Count("visita")
        )
    )

    if busqueda:
        clientes = clientes.filter(
            Q(nombre__icontains=busqueda)
            | Q(telefono__icontains=busqueda)
            | Q(usuario__email__icontains=busqueda)
        )

    clientes = clientes.order_by(
        "nombre", "id_cliente"
    )

    pagina = Paginator(clientes, 10).get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "inmuebles/clientes/listar.html",
        {
            "clientes": pagina,
            "busqueda": busqueda,
            "puede_eliminar": (
                es_administrador_clientes(request.user)
                and request.user.has_perm(
                    "inmuebles.delete_inmueble"
                )
            ),
        }
    )


@login_required
@permission_required(
    "inmuebles.add_inmueble",
    raise_exception=True
)
def registrar_cliente(request):

    verificar_personal_interno(request.user)

    formulario = ClienteForm(
        request.POST or None
    )

    if request.method == "POST" and formulario.is_valid():
        try:
            cliente = crear_cliente(formulario)

        except (IntegrityError, DatabaseError):
            formulario.add_error(
                None,
                "No fue posible registrar el cliente."
            )

        else:
            messages.success(
                request,
                "Cliente registrado correctamente."
            )

            return redirect(
                "inmuebles:detalle_cliente",
                cliente_id=cliente.pk
            )

    return render(
        request,
        "inmuebles/clientes/formulario.html",
        {
            "formulario": formulario,
            "modo": "crear",
        }
    )


@login_required
@permission_required(
    "inmuebles.change_inmueble",
    raise_exception=True
)
def editar_cliente(request, cliente_id):

    verificar_personal_interno(request.user)

    cliente = get_object_or_404(
        Cliente,
        pk=cliente_id
    )

    formulario = ClienteForm(
        request.POST or None,
        instance=cliente
    )

    if request.method == "POST" and formulario.is_valid():
        try:
            actualizar_cliente(
                cliente.pk,
                formulario
            )

        except (IntegrityError, DatabaseError):
            formulario.add_error(
                None,
                "No fue posible actualizar el cliente."
            )

        else:
            messages.success(
                request,
                "Cliente actualizado correctamente."
            )

            return redirect(
                "inmuebles:detalle_cliente",
                cliente_id=cliente.pk
            )

    return render(
        request,
        "inmuebles/clientes/formulario.html",
        {
            "formulario": formulario,
            "modo": "editar",
            "cliente": cliente,
        }
    )


@login_required
@permission_required(
    "inmuebles.view_inmueble",
    raise_exception=True
)
def detalle_cliente(request, cliente_id):

    verificar_personal_interno(request.user)

    cliente = get_object_or_404(
        Cliente.objects.select_related("usuario"),
        pk=cliente_id
    )

    visitas = (
        Visita.objects
        .filter(id_cliente_id=cliente.pk)
        .select_related("id_inmueble")
        .order_by("-fecha_hora")
    )

    administrador = es_administrador_clientes(
        request.user
    )

    return render(
        request,
        "inmuebles/clientes/detalle.html",
        {
            "cliente": cliente,
            "visitas": visitas,
            "puede_editar": request.user.has_perm(
                "inmuebles.change_inmueble"
            ),
            "puede_vincular": (
                administrador
                and request.user.has_perm(
                    "inmuebles.change_inmueble"
                )
            ),
            "puede_eliminar": (
                administrador
                and request.user.has_perm(
                    "inmuebles.delete_inmueble"
                )
                and not visitas.exists()
            ),
        }
    )


@login_required
@permission_required(
    "inmuebles.change_inmueble",
    raise_exception=True
)
def vincular_cuenta_cliente(request, cliente_id):

    if not es_administrador_clientes(request.user):
        raise PermissionDenied

    cliente = get_object_or_404(
        Cliente,
        pk=cliente_id
    )

    formulario = VincularUsuarioClienteForm(
        request.POST or None,
        cliente=cliente
    )

    if request.method == "POST" and formulario.is_valid():

        try:
            vincular_usuario(
                cliente.pk,
                formulario.cleaned_data["usuario"]
            )

        except ValidationError as error:
            formulario.add_error(
                "usuario",
                " ".join(error.messages)
            )

        except (IntegrityError, DatabaseError):
            formulario.add_error(
                "usuario",
                "No fue posible vincular la cuenta."
            )

        else:
            messages.success(
                request,
                "La vinculación se actualizó correctamente."
            )

            return redirect(
                "inmuebles:detalle_cliente",
                cliente_id=cliente.pk
            )

    return render(
        request,
        "inmuebles/clientes/vincular.html",
        {
            "cliente": cliente,
            "formulario": formulario,
        }
    )


@login_required
@permission_required(
    "inmuebles.delete_inmueble",
    raise_exception=True
)
@require_POST
def borrar_cliente(request, cliente_id):

    if not es_administrador_clientes(request.user):
        raise PermissionDenied

    try:
        nombre = eliminar_cliente(cliente_id)

    except Cliente.DoesNotExist:
        messages.error(
            request,
            "El cliente ya no existe."
        )

    except ValidationError as error:
        messages.error(
            request,
            " ".join(error.messages)
        )

    except (IntegrityError, DatabaseError):
        messages.error(
            request,
            "No fue posible eliminar el cliente."
        )

    else:
        messages.success(
            request,
            f"El cliente {nombre} fue eliminado."
        )

    return redirect("inmuebles:clientes")

