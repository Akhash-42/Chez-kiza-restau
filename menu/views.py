from django.shortcuts import render
from .models import Plat


def landing(request):
    return render(request, 'landing.html')


def liste_plats(request):
    plats = Plat.objects.filter(disponible=True)
    return render(request, 'menu/liste.html', {'plats': plats})


def settings_page(request):
    return render(request, 'settings.html')
