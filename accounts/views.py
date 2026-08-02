from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


def _get_next(request):
    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url and next_url.startswith('/'):
        return next_url
    return 'liste_plats'


def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(_get_next(request))
    else:
        form = UserCreationForm()
    return render(request, 'accounts/inscription.html', {'form': form, 'next': request.GET.get('next', '')})


def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(_get_next(request))
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/connexion.html', {'form': form, 'next': request.GET.get('next', '')})


def deconnexion(request):
    logout(request)
    return redirect('liste_plats')
