from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from menu.models import Plat
from .models import Commande, LigneCommande


@login_required
def panier(request):
    panier = request.session.get('panier', {})
    items = []
    total = 0
    for plat_id, quantite in panier.items():
        plat = get_object_or_404(Plat, id=plat_id)
        sous_total = plat.prix * quantite
        total += sous_total
        items.append({'plat': plat, 'quantite': quantite, 'sous_total': sous_total})
    return render(request, 'orders/panier.html', {'panier': items, 'total': total})


@login_required
def ajouter_au_panier(request, plat_id):
    get_object_or_404(Plat, id=plat_id)
    panier = request.session.get('panier', {})
    plat_id_str = str(plat_id)
    panier[plat_id_str] = panier.get(plat_id_str, 0) + 1
    request.session['panier'] = panier
    return redirect(request.META.get('HTTP_REFERER', 'liste_plats'))


@login_required
def valider_commande(request):
    panier = request.session.get('panier', {})
    if not panier:
        return redirect('panier')

    if request.method == 'POST':
        quartier = request.POST.get('quartier')
        numero = request.POST.get('numero')
        commande = Commande.objects.create(
            client=request.user,
            statut='en_preparation',
            adresse=numero,
            quartier=quartier,
        )
        for plat_id, quantite in panier.items():
            plat = get_object_or_404(Plat, id=plat_id)
            LigneCommande.objects.create(commande=commande, plat=plat, quantite=quantite)

        request.session['panier'] = {}
        return redirect('confirmation', commande_id=commande.id)

    return render(request, 'orders/valider.html')


@login_required
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

    delivery_fee = 1500
    subtotal = 0
    for plat_id_key, quantite in panier.items():
        plat_obj = get_object_or_404(Plat, id=plat_id_key)
        subtotal += plat_obj.prix * quantite

    response_data = {
        'count': sum(panier.values()),
        'subtotal': f'{subtotal} FCFA',
        'delivery': f'{delivery_fee} FCFA',
        'total': f'{subtotal + delivery_fee} FCFA',
        'empty': not bool(panier),
    }

    if action in ['increase', 'decrease'] and quantity > 0:
        response_data['quantity'] = quantity
        response_data['item_subtotal'] = f'{plat.prix * quantity} FCFA'
    else:
        response_data['quantity'] = 0
        response_data['item_subtotal'] = '0 FCFA'

    return JsonResponse(response_data)


@login_required
def confirmation(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id, client=request.user)
    return render(request, 'orders/confirmation.html', {'commande': commande})


@login_required
def mes_commandes(request):
    commandes = Commande.objects.filter(client=request.user).order_by('-cree_le')
    commandes_data = []
    for commande in commandes:
        total = sum(l.total for l in commande.lignes.all())
        commandes_data.append({'commande': commande, 'total': total})
    return render(request, 'orders/mes_commandes.html', {'commandes_data': commandes_data})
