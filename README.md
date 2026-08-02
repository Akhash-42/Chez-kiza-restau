# 🍽️ Chez Kiza

<p align="center">
  <img src="menu/static/menu/images/logo.jpg" alt="Chez Kiza Logo" width="120" style="border-radius: 50%;">
</p>

<p align="center">
  <strong>Commandez vos repas préférés, livrés directement chez vous… ou à savourer sur place.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Django-6.0-green?style=flat-square&logo=django" />
  <img src="https://img.shields.io/badge/TailwindCSS-4.x-blue?style=flat-square&logo=tailwindcss" />
  <img src="https://img.shields.io/badge/DaisyUI-5.x-purple?style=flat-square" />
  <img src="https://img.shields.io/badge/Python-3.x-yellow?style=flat-square&logo=python" />
</p>

---

## 📖 Description

**Chez Kiza** est une application web de commande de repas en ligne. Les clients peuvent parcourir le menu, ajouter des plats au panier, passer une commande en **livraison à domicile** ou **sur place**, puis **suivre son statut en temps réel**. L'interface est mobile-first, moderne et rapide.

---

## 🛠️ Technologies utilisées

| Technologie | Rôle |
|---|---|
| **Django 6** | Backend, ORM, authentification |
| **Tailwind CSS 4** | Styles utilitaires mobile-first |
| **DaisyUI 5** | Composants UI (cards, navbar, badges...) |
| **SQLite** | Base de données (développement) |
| **JavaScript** | Animation panier, badge localStorage, suivi temps réel |

---

## ✅ Fonctionnalités

- 🔐 Inscription et connexion utilisateur (avec redirection intelligente `?next=`)
- 🍽️ Affichage du menu avec images, descriptions, prix et **détection auto des allergènes / épicé**
- 🛒 Panier en session : fonctionne **sans connexion**, ajout avec animation et badge compteur
- 📦 Commande **livraison** (quartier, adresse, téléphone) ou **sur place** (nombre de personnes)
- 📋 Historique des commandes avec statuts colorés et montant total calculé côté serveur
- 🛰️ **Suivi de commande en temps réel** (frise chronologique + rafraîchissement automatique)
- 🔧 Interface d'administration Django : statut éditable directement dans la liste + actions groupées
- 🎨 3 thèmes (Kiza, Clair, Éco) avec contrastes corrigés pour chaque thème

---

## 🚀 Installation

### 1. Cloner le projet

```bash
git clone https://github.com/<votre-username>/chez-kiza.git
cd chez-kiza/Chez-kiza-restau
```

### 2. Créer et activer l'environnement virtuel

```bash
python -m venv env

# Windows
env\Scripts\activate

# macOS / Linux
source env/bin/activate
```

### 3. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

### 4. Installer Tailwind CSS et DaisyUI

```bash
python manage.py tailwind install
```

### 5. Appliquer les migrations

```bash
python manage.py migrate
```

### 6. Créer un superutilisateur (admin)

```bash
python manage.py createsuperuser
```

### 7. Lancer le serveur Tailwind (dans un terminal séparé)

```bash
python manage.py tailwind start
```

> Pour un build de production du CSS : `python manage.py tailwind build`

### 8. Lancer le serveur Django

```bash
python manage.py runserver
```

Accéder à l'app : [http://127.0.0.1:8000](http://127.0.0.1:8000)
Admin : [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## 📦 Structure du projet

```
Chez-kiza-restau/
├── accounts/        # Inscription, connexion, déconnexion
├── menu/            # Plats, liste du menu, filtres (templatetags/money)
├── orders/          # Panier, commandes, suivi, historique
├── theme/           # Tailwind CSS + DaisyUI + thèmes
├── templates/       # Templates globaux (landing)
├── kiza/            # Settings, URLs principales
├── media/           # Images uploadées (plats)
└── manage.py
```

---

## 🛰️ Suivi des commandes

Le client peut suivre chaque commande en temps réel :

1. **Au client** : après validation, un bouton « Suivre ma commande » mène à une page dédiée
   (`/orders/suivi/<id>/`) avec une **frise chronologique** :
   - Livraison : Commande reçue → En livraison → Livrée
   - Sur place : Commande reçue → Prête à être servie → Servie
   - La page interroge automatiquement `/orders/suivi/<id>/json/` **toutes les 5 secondes**
     et met à jour badge, message et frise sans recharger la page.
2. **Au restaurant** (admin) : le statut se change en 2 clics dans la liste
   `/admin/orders/commande/` :
   - Colonne « Statut » **éditable directement** dans la liste (menu déroulant).
   - Actions groupées : « Marquer : En préparation », « En livraison », « Prête à être servie »,
     « Livrée / Servie », « Annulée » (sélection multiple).
   - Un lien « Voir le suivi » ouvre la page client correspondante.

---

## 🧪 Tests

```bash
python manage.py test
```

Les tests couvrent : panier invité, ajout/modification/suppression, calculs des prix,
validation livraison/sur place, protection des accès (404 sur les commandes d'autrui),
rendu du suivi et mise à jour du statut.

---

## ⚙️ Configuration (variables d'environnement)

| Variable | Défaut | Rôle |
|---|---|---|
| `DJANGO_SECRET_KEY` | clé de dev | Clé secrète (à changer en prod) |
| `DJANGO_DEBUG` | `True` | Mode debug (mettre `False` en prod) |
| `DJANGO_ALLOWED_HOSTS` | `127.0.0.1,localhost` | Hôtes autorisés |
| `NPM_BIN_PATH` | `/usr/bin/npm` | Chemin vers npm |

Le frais de livraison est centralisé dans `kiza/settings.py` (`DELIVERY_FEE = 1500`).

---

## 📸 Captures d'écran

> 🚧 À venir...

| Page | Aperçu |
|---|---|
| Landing page | _à venir_ |
| Menu | _à venir_ |
| Panier | _à venir_ |
| Suivi de commande | _à venir_ |

---

## 👨‍💻👩‍💻 Auteur

Fait avec ❤️ par l'équipe **OpenMind Academy**
