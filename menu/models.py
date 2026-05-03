from django.db import models


class Plat(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='plats/', blank=True, null=True)
    disponible = models.BooleanField(default=True)
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom
