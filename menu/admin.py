from django.contrib import admin
from .models import Plat


@admin.register(Plat)
class PlatAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'disponible', 'cree_le')
    list_filter = ('disponible',)
    search_fields = ('nom',)
