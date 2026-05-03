# 🍽️ Chez Kiza

<p align="center">
  <img src="menu/static/menu/images/logo.jpg" alt="Chez Kiza Logo" width="120" style="border-radius: 50%;">
</p>

<p align="center">
  <strong>Commandez vos repas préférés, livrés directement chez vous.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Django-6.0-green?style=flat-square&logo=django" />
  <img src="https://img.shields.io/badge/TailwindCSS-4.x-blue?style=flat-square&logo=tailwindcss" />
  <img src="https://img.shields.io/badge/DaisyUI-5.x-purple?style=flat-square" />
  <img src="https://img.shields.io/badge/Python-3.x-yellow?style=flat-square&logo=python" />
</p>

---

## 📖 Description

**Chez Kiza** est une application web de commande de repas en ligne. Les clients peuvent parcourir le menu, ajouter des plats au panier, passer une commande et suivre son statut. L'interface est mobile-first, moderne et rapide.

---

## 🛠️ Technologies utilisées

| Technologie | Rôle |
|---|---|
| **Django 6** | Backend, ORM, authentification |
| **Tailwind CSS 4** | Styles utilitaires mobile-first |
| **DaisyUI 5** | Composants UI (cards, navbar, badges...) |
| **SQLite** | Base de données (développement) |
| **JavaScript** | Animation panier, badge localStorage |

---

## ✅ Fonctionnalités MVP

- 🔐 Inscription et connexion utilisateur
- 🍽️ Affichage du menu avec images, descriptions et prix
- 🛒 Ajout au panier avec animation et badge compteur
- 📦 Validation de commande avec adresse et quartier
- 📋 Historique des commandes avec statuts colorés
- 🔧 Interface d'administration Django (gestion plats, commandes)

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
pip install django django-tailwind pillow
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

### 8. Lancer le serveur Django

```bash
python manage.py runserver
```

Accéder à l'app : [http://127.0.0.1:8000](http://127.0.0.1:8000)
Admin : [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## 📁 Structure du projet

```
Chez-kiza-restau/
├── accounts/        # Inscription, connexion
├── menu/            # Plats, liste du menu
├── orders/          # Panier, commandes, historique
├── theme/           # Tailwind CSS + DaisyUI
├── templates/       # Templates globaux (landing)
├── kiza/            # Settings, URLs principales
└── manage.py
```

---

## 📸 Captures d'écran

> 🚧 À venir...

| Page | Aperçu |
|---|---|
| Landing page | _à venir_ |
| Menu | _à venir_ |
| Panier | _à venir_ |
| Mes commandes | _à venir_ |

---

## 👨‍🍳 Auteur

Fait avec ❤️ par l'équipe **OpenMind Academy**
