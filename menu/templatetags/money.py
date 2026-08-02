from django import template

register = template.Library()


@register.filter
def fcf(value):
    """Formate un montant en FCFA : 2500.00 -> '2 500', 2500.50 -> '2 500.50'."""
    try:
        value = float(value)
    except (TypeError, ValueError):
        return value
    if value.is_integer():
        formatted = f"{int(value):,}".replace(',', ' ')
    else:
        formatted = f"{value:,.2f}".replace(',', ' ')
    return formatted
