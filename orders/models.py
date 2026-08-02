from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from menu.models import Plat


class Commande(models.Model):
    TYPE_COMMANDE = [
        ('livraison', 'Livraison à domicile'),
        ('sur_place', 'Sur place'),
    ]

    STATUTS = [
        ('en_preparation', 'En préparation'),
        ('en_livraison', 'En livraison'),
        ('prete', 'Prête à être servie'),
        ('livree', 'Livrée / Servie'),
        ('annulee', 'Annulée'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    type_commande = models.CharField(max_length=20, choices=TYPE_COMMANDE, default='livraison')
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_preparation')
    adresse = models.CharField(max_length=300, blank=True)
    quartier = models.CharField(max_length=100, blank=True)
    telephone = models.CharField(max_length=30, blank=True)
    nb_personnes = models.PositiveIntegerField(null=True, blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)

    @property
    def est_sur_place(self):
        return self.type_commande == 'sur_place'

    @property
    def sous_total(self):
        return sum(l.total for l in self.lignes.all())

    @property
    def frais_livraison(self):
        return 0 if self.est_sur_place else settings.DELIVERY_FEE

    @property
    def total(self):
        return self.sous_total + self.frais_livraison

    def __str__(self):
        return f"Commande #{self.pk} - {self.client.username}"


class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='lignes')
    plat = models.ForeignKey(Plat, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()

    @property
    def total(self):
        return self.plat.prix * self.quantite

    def __str__(self):
        return f"{self.quantite}x {self.plat.nom}"
