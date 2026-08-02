from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from menu.models import Plat
from .models import Commande, LigneCommande
from .cart import get_cart_items, get_cart_mode, delivery_fee_for, cart_totals, to_number


def panier(request):
    items = get_cart_items(request.session)
    mode = get_cart_mode(request.session)
    total = to_number(sum(item['sous_total'] for item in items))
    return render(request, 'orders/panier.html', {
        'panier': items,
        'total': total,
        'mode': mode,
        'delivery_fee': delivery_fee_for(mode),
    })


def ajouter_au_panier(request, plat_id):
    get_object_or_404(Plat, id=plat_id, disponible=True)
    panier = request.session.get('panier', {})
    panier[str(plat_id)] = panier.get(str(plat_id), 0) + 1
    request.session['panier'] = panier
    return redirect(request.META.get('HTTP_REFERER', 'liste_plats'))


@login_required
def valider_commande(request):
    cart = cart_totals(request.session)
    if not cart['items']:
        return redirect('liste_plats')

    if request.method == 'POST':
        mode = request.POST.get('type_commande', 'livraison')
        if mode not in ('livraison', 'sur_place'):
            mode = 'livraison'

        quartier = (request.POST.get('quartier') or '').strip()
        adresse = (request.POST.get('adresse') or '').strip()
        telephone = (request.POST.get('telephone') or '').strip()
        nb_personnes = request.POST.get('nb_personnes') or None

        errors = []
        if mode == 'livraison':
            if not quartier:
                errors.append("Veuillez renseigner votre quartier.")
            if not adresse:
                errors.append("Veuillez renseigner votre adresse.")
            if not telephone:
                errors.append("Veuillez renseigner votre numéro de téléphone.")
        else:
            if nb_personnes:
                try:
                    nb_personnes = int(nb_personnes)
                    if nb_personnes < 1 or nb_personnes > 20:
                        errors.append("Nombre de personnes invalide.")
                except ValueError:
                    errors.append("Nombre de personnes invalide.")
            else:
                nb_personnes = None

        if errors:
            return render(request, 'orders/valider.html', {
                'cart': cart,
                'errors': errors,
                'type_commande': mode,
                'delivery_fee': settings.DELIVERY_FEE,
            })

        commande = Commande.objects.create(
            client=request.user,
            type_commande=mode,
            statut='en_preparation',
            adresse=adresse,
            quartier=quartier,
            telephone=telephone,
            nb_personnes=nb_personnes,
        )
        for plat_id, quantite in request.session.get('panier', {}).items():
            try:
                plat = Plat.objects.get(id=plat_id)
            except (Plat.DoesNotExist, ValueError):
                continue
            LigneCommande.objects.create(commande=commande, plat=plat, quantite=quantite)

        request.session['panier'] = {}
        return redirect('confirmation', commande_id=commande.id)

    return render(request, 'orders/valider.html', {
        'cart': cart,
        'type_commande': cart['mode'],
        'delivery_fee': settings.DELIVERY_FEE,
    })


def modifier_panier(request, plat_id, action):
    plat = get_object_or_404(Plat, id=plat_id)
    panier = request.session.get('panier', {})
    plat_id_str = str(plat_id)
    quantity = panier.get(plat_id_str, 0)

    if action == 'increase':
        quantity += 1
        panier[plat_id_str] = quantity
    elif action == 'decrease':
        if quantity > 1:
            quantity -= 1
            panier[plat_id_str] = quantity
    elif action == 'remove':
        panier.pop(plat_id_str, None)
        quantity = 0

    request.session['panier'] = panier

    cart = cart_totals(request.session)

    response_data = {
        'count': cart['count'],
        'subtotal': cart['subtotal'],
        'delivery': cart['delivery'],
        'total': cart['total'],
        'empty': not bool(panier),
        'mode': cart['mode'],
    }

    if action in ('increase', 'decrease') and quantity > 0:
        response_data['quantity'] = quantity
        response_data['item_subtotal'] = to_number(plat.prix * quantity)
    else:
        response_data['quantity'] = 0
        response_data['item_subtotal'] = 0

    return JsonResponse(response_data)


@login_required
def confirmation(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id, client=request.user)
    return render(request, 'orders/confirmation.html', {'commande': commande})


@login_required
def mes_commandes(request):
    commandes = Commande.objects.filter(client=request.user).order_by('-cree_le')
    return render(request, 'orders/mes_commandes.html', {'commandes': commandes})


@login_required
def suivi_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id, client=request.user)
    return render(request, 'orders/suivi.html', {'commande': commande})


@login_required
def suivi_commande_json(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id, client=request.user)
    return JsonResponse({
        'statut': commande.statut,
        'statut_display': commande.get_statut_display(),
        'type_commande': commande.type_commande,
    })
