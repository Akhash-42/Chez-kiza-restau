from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Commande, LigneCommande


class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 0
    readonly_fields = ('plat', 'quantite')


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'type_commande', 'statut', 'quartier', 'total', 'cree_le', 'suivre_lien')
    list_filter = ('statut', 'type_commande')
    list_editable = ('statut',)
    search_fields = ('client__username', 'quartier', 'adresse', 'telephone')
    list_per_page = 25
    inlines = [LigneCommandeInline]
    readonly_fields = ('client', 'type_commande', 'cree_le', 'sous_total', 'frais_livraison', 'total')

    @admin.display(description='Total')
    def total(self, obj):
        return f"{obj.total} FCFA"

    @admin.display(description='Suivi')
    def suivre_lien(self, obj):
        return format_html('<a href="{}" target="_blank">Voir le suivi</a>', reverse('suivi_commande', args=[obj.pk]))

    actions = ['marquer_preparation', 'marquer_livraison', 'marquer_prete', 'marquer_livree', 'marquer_annulee']

    @admin.action(description='Marquer : En préparation')
    def marquer_preparation(self, request, queryset):
        queryset.update(statut='en_preparation')

    @admin.action(description='Marquer : En livraison')
    def marquer_livraison(self, request, queryset):
        queryset.update(statut='en_livraison')

    @admin.action(description='Marquer : Prête à être servie')
    def marquer_prete(self, request, queryset):
        queryset.update(statut='prete')

    @admin.action(description='Marquer : Livrée / Servie')
    def marquer_livree(self, request, queryset):
        queryset.update(statut='livree')

    @admin.action(description='Marquer : Annulée')
    def marquer_annulee(self, request, queryset):
        queryset.update(statut='annulee')
