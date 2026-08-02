from django.db import models

ALLERGEN_TERMS = {
    'arachides': ['arachide', 'cacahuete', 'cacahuète'],
    'gluten': ['gluten', 'farine', 'blé', 'ble'],
    'lait': ['lait', 'fromage', 'crème', 'creme', 'beurre', 'yaourt'],
    'œufs': ['œuf', 'oeuf', 'omelette'],
    'poisson': ['poisson', 'thon', 'saumon', 'sardine'],
    'fruits de mer': ['crevette', 'crabe', 'fruit de mer', 'homard'],
}


class Plat(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='plats/', blank=True, null=True)
    disponible = models.BooleanField(default=True)
    cree_le = models.DateTimeField(auto_now_add=True)

    SPICY_TERMS = ['epic', 'épic', 'piment', 'poivre', 'piquant']

    @property
    def is_spicy(self):
        description = (self.description or '').lower()
        return any(term in description for term in self.SPICY_TERMS)

    @property
    def allergens(self):
        description = (self.description or '').lower()
        return [label for label, terms in ALLERGEN_TERMS.items() if any(term in description for term in terms)]

    @property
    def allergen_label(self):
        return ', '.join(self.allergens) if self.allergens else 'Allergènes'

    def __str__(self):
        return self.nom
