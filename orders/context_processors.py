from menu.models import Plat


def cart_context(request):
    panier = request.session.get('panier', {})
    items = []
    total = 0
    for plat_id, quantite in panier.items():
        try:
            plat = Plat.objects.get(id=plat_id)
        except Plat.DoesNotExist:
            continue
        sous_total = plat.prix * quantite
        total += sous_total
        items.append({'plat': plat, 'quantite': quantite, 'sous_total': sous_total})

    delivery_fee = 1500
    cart_count = sum(item['quantite'] for item in items)
    return {
        'cart_items': items,
        'cart_subtotal': total,
        'cart_delivery_fee': delivery_fee,
        'cart_total': total + delivery_fee,
        'cart_count': cart_count,
    }
