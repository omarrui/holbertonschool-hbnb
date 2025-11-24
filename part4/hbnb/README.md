# HBnB – Évolutions Récentes (Part 4)

Ce document résume tout ce que nous venons d'implémenter dans cette phase : thème visuel dark fantasy, gestion avancée des avis (reviews), administration, suppression et mise à jour des lieux (places), commandes de maintenance, et correctifs divers.

## 1. Aperçu Général
L'application HBnB (Flask + SQLAlchemy + Flask-RESTX + JWT) expose une API REST et une interface dynamique (JS) pour :
- Créer / afficher des lieux
- Gérer des hôtes (users) et leurs propriétés
- Laisser des reviews avec notation étoilée
- Administrer (promotion, suppression de contenu)

## 2. Nouvelles Fonctionnalités Clés
### Thème & UI
- Palette "dark fantasy" appliquée (CSS refactor: couleurs, ombres, boutons).
- Cartes de lieux cliquables, affichage image, prix, moyenne des notes.
- Système d’étoiles dynamique (plein, demi, vide) calculé côté backend et rendu côté frontend.

### Images & Descriptions
- Colonne `image_filename` ajoutée (migration runtime si absent).
- Commande CLI `assign-image` pour associer une image statique à une place.
- Commande CLI `set-description` pour réécrire les descriptions dans le style du thème.

### Reviews
- Notation via étoiles interactives (JS) au lieu d’un `<select>`.
- Commentaire devenu optionnel (backend accepte chaîne vide; champ nullable).
- Prévention des doublons et auto‑review (un user ne review pas sa propre place, sauf admin).
- Suppression de review immédiate (✖) réservée à l’auteur ou à un admin (bouton ajouté + AJAX DELETE `/api/v1/reviews/<id>`).

### Places
- Boutons de suppression pour les places sur index et page détail (DELETE `/api/v1/places/<id>`).
- Création de place corrigée : `owner_id`, `latitude`, `longitude` sont optionnels dans le modèle REST; `owner_id` est auto‑assigné au user connecté si non fourni.

### Administration
- Champ `User.is_admin` inclus dans le token JWT (`is_admin` claim).
- Promotion / rétrogradation via CLI : `promote-user`, `demote-user`, `list-users`.
- Admin peut : dépasser limites review (doublon, self) et supprimer n’importe quel review ou place.

### Commandes CLI Ajoutées / Étendues (`tools/manage.py`)
| Commande | Rôle |
|----------|------|
| `list-places` | Lister toutes les places (id, image, host). |
| `set-description --place-id --description` | Mettre à jour description d’une place. |
| `assign-image --place-id --image [--rename]` | Associer fichier image + renommer. |
| `reassign-host --place-id --host-email` | Changer l’hôte d’une place. |
| `add-host --email --first --last --password` | Créer un nouvel hôte. |
| `add-place --host-email --name --description --price [--amenities ...]` | Ajouter une place côté CLI. |
| `rename-host --email --first --last` | Renommer un hôte. |
| `promote-user --email` | Rendre un user admin. |
| `demote-user --email` | Retirer droits admin. |
| `list-users` | Lister tous les users avec statut admin. |

## 3. Sécurité & Validation
- `rating` forcé à un entier 1–5 (backend).
- `comment` peut être vide, jamais requis pour une review.
- Restrictions review : pas de doublon ni d’auto‑review (sauf admin).
- Validation géographique sur latitude/longitude si fournis.
- Protection simple contre traversal d’images (`assign-image` refuse `/` ou `\`).

## 4. Flux Frontend (JS `scripts.js`)
- Décodage JWT côté client pour extraire `is_admin` / `user_id` (base64 payload) et afficher les bons boutons.
- Suppression review/place via fetch DELETE + mise à jour DOM sans reload.
- Interaction étoiles (mouseover/keydown + sélection persistante).

## 5. Endpoints Principaux (Résumé)
| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api/v1/places/` | Liste des places (+ average_rating, review_count). |
| POST | `/api/v1/places/` | Créer place (auth; owner auto). |
| GET | `/api/v1/places/<id>` | Détail place + reviews + host. |
| PUT | `/api/v1/places/<id>` | Mettre à jour (owner ou admin). |
| DELETE | `/api/v1/places/<id>` | Supprimer (admin). |
| POST | `/api/v1/reviews/` | Créer review (auth; vérifs). |
| DELETE | `/api/v1/reviews/<id>` | Supprimer (auteur ou admin). |
| POST | `/api/v1/auth/register` | Inscription user. |
| POST | `/api/v1/auth/login` | Login (retour token). |

## 6. Guide Rapide
### Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r part4/hbnb/requirements.txt
python3 part4/hbnb/run.py  # Démarre dev server
```

### Créer une place (UI)
1. Se connecter (login) pour obtenir cookie `token`.
2. Aller sur page création (`/create_place`).
3. Remplir *Title* et *Price* (latitude/longitude optionnels) > Submit.

### Créer une place (CLI)
```bash
python3 part4/hbnb/tools/manage.py add-place \
	--host-email host@example.com \
	--name "Tour des Brumes" \
	--description "Sommet noyé dans un brouillard ancien" \
	--price 120
```

### Assigner une image
```bash
python3 part4/hbnb/tools/manage.py assign-image --place-id <UUID> --image "Anor Londo.avif" --rename "Anor Londo"
```

### Modifier la description
```bash
python3 part4/hbnb/tools/manage.py set-description --place-id <UUID> --description "Nouvelle ambiance gothique sombre"
```

### Promouvoir un user en admin
```bash
python3 part4/hbnb/tools/manage.py promote-user --email jin@gmail.com
```

### Supprimer une review (UI)
Clique sur boutons de suppression (admin ou auteur) sur la carte review.

### Supprimer une place (UI)
Admin : Boutons de suppressionsur carte dans l’index OU “Delete Place” sur page détail.


## 7. Résumé Technique Rapide
- Front: Vanilla JS (fetch API, DOM incremental updates).
- Back: Flask Blueprints via Flask-RESTX (namespaces), JWT (flask-jwt-extended).
- ORM: SQLAlchemy (runtime ajout colonne image si manquante).
- Auth: Token stocké en cookie `token`, décodé côté JS pour privilèges.
- Patterns: Façade (`facade.py`) pour encapsuler logique de validation & dépôt.

## 8. Commandes de Maintenance (Rappel)
```bash
# Lister places
python3 part4/hbnb/tools/manage.py list-places

# Lister users
python3 part4/hbnb/tools/manage.py list-users

# Réassigner host
python3 part4/hbnb/tools/manage.py reassign-host --place-id <UUID> --host-email new@example.com
```

---
**Auteur:** Wassef ADALLAH
