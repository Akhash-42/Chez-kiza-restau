from django.urls import path
from . import views

urlpatterns = [
    path('panier/', views.panier, name='panier'),
    path('ajouter/<int:plat_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('modifier/<str:action>/<int:plat_id>/', views.modifier_panier, name='modifier_panier'),
    path('valider/', views.valider_commande, name='valider_commande'),
    path('confirmation/<int:commande_id>/', views.confirmation, name='confirmation'),
    path('mes-commandes/', views.mes_commandes, name='mes_commandes'),
]
