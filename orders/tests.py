from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from menu.models import Plat
from orders.models import Commande, LigneCommande


class PlatModelTests(TestCase):
    def test_allergens_detected_from_description(self):
        plat = Plat.objects.create(
            nom="Sauce arachide", description="Poulet à la sauce arachide et riz", prix=2000
        )
        self.assertIn('arachides', plat.allergens)
        self.assertTrue(plat.allergen_label)

    def test_no_allergens(self):
        plat = Plat.objects.create(nom="Brochettes", description="Brochettes de viande grillée", prix=1500)
        self.assertEqual(plat.allergens, [])
        self.assertEqual(plat.allergen_label, 'Allergènes')

    def test_is_spicy(self):
        plat = Plat.objects.create(nom="Pimenté", description="Très épicé au piment", prix=1800)
        self.assertTrue(plat.is_spicy)
        plat2 = Plat.objects.create(nom="Douce", description="Doux et crémeux", prix=1800)
        self.assertFalse(plat2.is_spicy)


class CartTests(TestCase):
    def setUp(self):
        self.plat = Plat.objects.create(nom="Okok", description="Okok aux épinards", prix=2500)

    def test_guest_can_add_to_cart(self):
        response = self.client.get(reverse('ajouter_au_panier', args=[self.plat.id]))
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        self.assertEqual(session['panier'][str(self.plat.id)], 1)

    def test_cart_page_works_for_guest(self):
        self.client.get(reverse('ajouter_au_panier', args=[self.plat.id]))
        response = self.client.get(reverse('panier'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Okok')

    def test_increase_quantity(self):
        self.client.get(reverse('ajouter_au_panier', args=[self.plat.id]))
        self.client.get(reverse('ajouter_au_panier', args=[self.plat.id]))
        session = self.client.session
        self.assertEqual(session['panier'][str(self.plat.id)], 2)

    def test_modifier_increase_returns_numbers(self):
        self.client.get(reverse('ajouter_au_panier', args=[self.plat.id]))
        response = self.client.post(reverse('modifier_panier', args=['increase', self.plat.id]))
        data = response.json()
        self.assertEqual(data['quantity'], 2)
        self.assertEqual(data['item_subtotal'], 5000)
        self.assertEqual(data['count'], 2)
        self.assertEqual(data['subtotal'], 5000)

    def test_modifier_remove(self):
        self.client.get(reverse('ajouter_au_panier', args=[self.plat.id]))
        response = self.client.post(reverse('modifier_panier', args=['remove', self.plat.id]))
        data = response.json()
        self.assertTrue(data['empty'])
        self.assertEqual(data['count'], 0)

    def test_cart_page_skips_missing_plat(self):
        missing_id = 99999
        session = self.client.session
        session['panier'] = {str(missing_id): 1}
        session.save()
        response = self.client.get(reverse('panier'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Votre panier est vide')


class OrderTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='client1', password='pass12345')
        self.plat = Plat.objects.create(nom="Attiéké", description="Attiéké poisson", prix=2500)

    def test_checkout_requires_login(self):
        response = self.client.get(reverse('valider_commande'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/connexion/', response.url)

    def test_checkout_login_redirect_back(self):
        self.client.get(reverse('ajouter_au_panier', args=[self.plat.id]))
        response = self.client.get(reverse('valider_commande'))
        self.assertIn('next', response.url)

    def test_livraison_order_creation(self):
        self.client.login(username='client1', password='pass12345')
        self.client.get(reverse('ajouter_au_panier', args=[self.plat.id]))
        response = self.client.post(reverse('valider_commande'), {
            'type_commande': 'livraison',
            'quartier': 'Cocody',
            'adresse': 'Rue des jardins',
            'telephone': '+225 0700000000',
        })
        self.assertEqual(response.status_code, 302)
        commande = Commande.objects.get()
        self.assertEqual(commande.type_commande, 'livraison')
        self.assertEqual(commande.quartier, 'Cocody')
        self.assertEqual(commande.total, 2500 + 1500)
        self.assertEqual(commande.lignes.count(), 1)
        self.assertEqual(commande.lignes.first().quantite, 1)

    def test_livraison_missing_fields_rejected(self):
        self.client.login(username='client1', password='pass12345')
        self.client.get(reverse('ajouter_au_panier', args=[self.plat.id]))
        response = self.client.post(reverse('valider_commande'), {
            'type_commande': 'livraison',
            'quartier': '',
            'adresse': '',
            'telephone': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Commande.objects.count(), 0)

    def test_sur_place_order_creation(self):
        self.client.login(username='client1', password='pass12345')
        self.client.get(reverse('ajouter_au_panier', args=[self.plat.id]))
        response = self.client.post(reverse('valider_commande'), {
            'type_commande': 'sur_place',
            'nb_personnes': '3',
        })
        self.assertEqual(response.status_code, 302)
        commande = Commande.objects.get()
        self.assertEqual(commande.type_commande, 'sur_place')
        self.assertTrue(commande.est_sur_place)
        self.assertEqual(commande.nb_personnes, 3)
        self.assertEqual(commande.total, 2500)

    def test_creation_clears_cart(self):
        self.client.login(username='client1', password='pass12345')
        self.client.get(reverse('ajouter_au_panier', args=[self.plat.id]))
        self.client.post(reverse('valider_commande'), {'type_commande': 'sur_place'})
        self.assertEqual(self.client.session.get('panier'), {})

    def test_user_cannot_see_other_users_order(self):
        other = User.objects.create_user(username='other', password='pass12345')
        commande = Commande.objects.create(client=other, type_commande='sur_place')
        self.client.login(username='client1', password='pass12345')
        self.assertEqual(self.client.get(reverse('confirmation', args=[commande.id])).status_code, 404)
        self.assertEqual(self.client.get(reverse('suivi_commande', args=[commande.id])).status_code, 404)


class SuiviTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='client1', password='pass12345')
        self.plat = Plat.objects.create(nom="Plat test", description="Description", prix=1000)

    def test_suivi_json_updates_status(self):
        self.client.login(username='client1', password='pass12345')
        self.client.get(reverse('ajouter_au_panier', args=[self.plat.id]))
        self.client.post(reverse('valider_commande'), {'type_commande': 'sur_place'})
        commande = Commande.objects.get()
        response = self.client.get(reverse('suivi_commande_json', args=[commande.id]))
        self.assertEqual(response.json()['statut'], 'en_preparation')

        commande.statut = 'livree'
        commande.save()
        response = self.client.get(reverse('suivi_commande_json', args=[commande.id]))
        self.assertEqual(response.json()['statut'], 'livree')

    def test_suivi_page_renders(self):
        self.client.login(username='client1', password='pass12345')
        self.client.get(reverse('ajouter_au_panier', args=[self.plat.id]))
        self.client.post(reverse('valider_commande'), {'type_commande': 'sur_place'})
        commande = Commande.objects.get()
        response = self.client.get(reverse('suivi_commande', args=[commande.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Progression')
