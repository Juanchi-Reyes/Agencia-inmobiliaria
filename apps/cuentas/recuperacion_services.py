
"""
Recuperación de contraseña simulada para entorno académico.

IMPORTANTE:
Este mecanismo NO acredita la identidad de una persona.
El código se muestra al solicitante en el mismo navegador.

Utilizar exclusivamente en desarrollo local.
"""

import secrets
import time

from django.contrib.auth.hashers import (
    make_password,
    check_password,
)
from django.contrib.auth import get_user_model


CLAVE_RECUPERACION = "recuperacion_demo"
CLAVE_CODIGO_VISIBLE = "recuperacion_demo_codigo_visible"
CLAVE_ULTIMA_SOLICITUD = "recuperacion_demo_ultima_solicitud"

DURACION_SEGUNDOS = 600
MAX_INTENTOS = 5
ESPERA_NUEVA_SOLICITUD = 60


def limpiar_recuperacion(request):
    """
    Elimina la solicitud actual de la sesión.
    No elimina el control de frecuencia.
    """

    request.session.pop(CLAVE_RECUPERACION, None)
    request.session.pop(CLAVE_CODIGO_VISIBLE, None)


def puede_solicitar_codigo(request):
    """
    Limita nuevas solicitudes desde la misma sesión.
    """

    ultima = request.session.get(
        CLAVE_ULTIMA_SOLICITUD, 0
    )

    transcurrido = time.time() - ultima

    restante = ESPERA_NUEVA_SOLICITUD - transcurrido

    return max(0, int(restante + 0.999))


def generar_codigo(request, usuario):
    """
    Genera un código de 6 dígitos.

    Guarda solamente el hash para la comprobación.
    El texto original se conserva temporalmente
    para mostrarlo una sola vez en la interfaz.
    """

    codigo = f"{secrets.randbelow(1_000_000):06d}"

    limpiar_recuperacion(request)

    request.session[CLAVE_RECUPERACION] = {
        "usuario_id": usuario.pk,
        "codigo_hash": make_password(codigo),
        "creado_en": int(time.time()),
        "intentos": 0,
        "verificado": False,

        # Invalida la solicitud si la contraseña
        # de la cuenta cambia mientras tanto.
        "hash_autenticacion": (
            usuario.get_session_auth_hash()
        ),
    }

    request.session[CLAVE_CODIGO_VISIBLE] = codigo

    request.session[CLAVE_ULTIMA_SOLICITUD] = time.time()

    return codigo


def obtener_estado(request):
    """
    Recupera la solicitud y valida:

    - existencia;
    - vencimiento;
    - existencia de la cuenta;
    - cuenta activa;
    - contraseña original sin cambios.
    """

    estado = request.session.get(
        CLAVE_RECUPERACION
    )

    if not isinstance(estado, dict):
        return None, None

    creado_en = estado.get("creado_en", 0)

    if (
        creado_en > time.time()
        or time.time() - creado_en > DURACION_SEGUNDOS
    ):
        limpiar_recuperacion(request)
        return None, None

    Usuario = get_user_model()

    usuario = Usuario.objects.filter(
        pk=estado.get("usuario_id"),
        is_active=True,
    ).first()

    if usuario is None:
        limpiar_recuperacion(request)
        return None, None

    if (
        estado.get("hash_autenticacion")
        != usuario.get_session_auth_hash()
    ):
        limpiar_recuperacion(request)
        return None, None

    return estado, usuario


def comprobar_codigo(request, codigo):
    """
    Comprueba el código y controla los intentos.

    Retorna (correcto, mensaje).
    """

    estado, usuario = obtener_estado(request)

    if estado is None:
        return False, "La solicitud expiró o ya no existe."

    if estado.get("verificado"):
        return True, "Código validado anteriormente."

    intentos = estado.get("intentos", 0)

    if intentos >= MAX_INTENTOS:
        limpiar_recuperacion(request)
        return False, "Agotaste los intentos permitidos."

    hash_guardado = estado.get("codigo_hash")

    if not hash_guardado:
        limpiar_recuperacion(request)
        return False, "El código ya no está disponible."

    correcto = check_password(
        codigo,
        hash_guardado
    )

    if correcto:
        estado["verificado"] = True

        # El código deja de ser reutilizable.
        estado.pop("codigo_hash", None)

        request.session[CLAVE_RECUPERACION] = estado

        return True, "Código verificado correctamente."

    intentos += 1
    estado["intentos"] = intentos

    if intentos >= MAX_INTENTOS:
        limpiar_recuperacion(request)

        return (
            False,
            "Agotaste los cinco intentos. "
            "Debes iniciar otra recuperación."
        )

    request.session[CLAVE_RECUPERACION] = estado

    restantes = MAX_INTENTOS - intentos

    return (
        False,
        f"Código incorrecto. "
        f"Te quedan {restantes} intentos."
    )
