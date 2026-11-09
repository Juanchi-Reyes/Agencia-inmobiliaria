
from django import template

register = template.Library()


@register.filter
def precio_cop(valor):
    """
    Convierte un precio al formato de pesos colombianos.

    Ejemplo:
    320000000 -> $320.000.000
    """

    if valor is None:
        return "Sin precio"

    numero = f"{valor:,.0f}"

    return "$" + numero.replace(",", ".")
