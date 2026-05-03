from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('menu/', views.liste_plats, name='liste_plats'),
]
