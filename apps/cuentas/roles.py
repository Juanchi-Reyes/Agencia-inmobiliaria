
def obtener_rol(usuario):
    """
    Devuelve el rol principal de un usuario.

    Prioridad:
    1. Administrador
    2. Vendedor
    3. Cliente
    """

    if not usuario.is_authenticated:
        return None

    if usuario.is_superuser:
        return "Administrador"

    grupos = set(
        usuario.groups.values_list("name", flat=True)
    )

    if "Administrador" in grupos:
        return "Administrador"

    if "Vendedor" in grupos:
        return "Vendedor"

    if "Cliente" in grupos:
        return "Cliente"

    return None
