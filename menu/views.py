from django.shortcuts import render
from .models import Plat


def landing(request):
    return render(request, 'landing.html')


def liste_plats(request):
    plats = list(Plat.objects.filter(disponible=True))
    for plat in plats:
        description = (plat.description or '').lower()
        plat.is_spicy = any(term in description for term in ['epic', 'épic', 'piment', 'poivre'])
        allergens = []
        if 'arachide' in description or 'cacahuete' in description:
            allergens.append('arachides')
        if 'gluten' in description:
            allergens.append('gluten')
        if 'lait' in description or 'fromage' in description or 'crème' in description:
            allergens.append('lait')
        if 'œuf' in description or 'oeuf' in description:
            allergens.append('œufs')
        plat.allergen_label = ', '.join(allergens) if allergens else 'Allergènes'
    return render(request, 'menu/liste.html', {'plats': plats})


def settings_page(request):
    return render(request, 'settings.html')
