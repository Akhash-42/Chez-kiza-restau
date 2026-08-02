from .cart import cart_totals


def cart_context(request):
    cart = cart_totals(request.session)
    return {
        'cart_items': cart['items'],
        'cart_mode': cart['mode'],
        'cart_subtotal': cart['subtotal'],
        'cart_delivery_fee': cart['delivery'],
        'cart_total': cart['total'],
        'cart_count': cart['count'],
    }
