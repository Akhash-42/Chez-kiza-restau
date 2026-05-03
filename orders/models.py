from django.db import models
from django.contrib.auth.models import User
from menu.models import Plat


class Commande(models.Model):
    STATUTS = [
        ('en_preparation', 'En préparation'),
        ('en_livraison', 'En livraison'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_preparation')
    adresse = models.CharField(max_length=300)
    quartier = models.CharField(max_length=100)
    cree_le = models.DateTimeField(auto_now_add=True)

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
