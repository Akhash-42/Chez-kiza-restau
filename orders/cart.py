from django.conf import settings
from menu.models import Plat


def to_number(value):
    """Convertit un Decimal en int (si entier) ou float pour la sérialisation JSON."""
    value = float(value)
    return int(value) if value.is_integer() else value


def get_cart_items(session):
    """Retourne la liste des articles du panier stocké en session (clés str -> quantité)."""
    panier = session.get('panier', {})
    items = []
    total = 0
    for plat_id, quantite in panier.items():
        try:
            plat = Plat.objects.get(id=plat_id)
        except (Plat.DoesNotExist, ValueError):
            continue
        sous_total = plat.prix * quantite
        total += sous_total
        items.append({'plat': plat, 'quantite': quantite, 'sous_total': sous_total})
    return items


def get_cart_mode(session):
    """Mode de commande courant : 'livraison' ou 'sur_place'."""
    mode = session.get('panier_mode', 'livraison')
    return mode if mode in ('livraison', 'sur_place') else 'livraison'


def delivery_fee_for(mode):
    return 0 if mode == 'sur_place' else settings.DELIVERY_FEE


def cart_totals(session):
    items = get_cart_items(session)
    mode = get_cart_mode(session)
    subtotal = to_number(sum(item['sous_total'] for item in items))
    delivery = to_number(delivery_fee_for(mode))
    return {
        'items': items,
        'mode': mode,
        'subtotal': subtotal,
        'delivery': delivery,
        'total': to_number(subtotal + delivery),
        'count': sum(item['quantite'] for item in items),
    }
