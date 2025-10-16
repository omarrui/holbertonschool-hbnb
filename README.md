# holbertonschool-hbnb

Projet HBnB

## Objectif
Implémenter des endpoints pour gérer les entités Place et Review.
## Dépendances
- Python 3.8+
- flask
- flask-restx

Installez les dépendances :

```powershell
pip install flask flask-restx
```

## Lancer l'application

```
python run.py
```

L'API sera disponible par défaut sur `http://127.0.0.1:5000/`. La documentation Swagger est exposée sur `http://127.0.0.1:5000/api/v1/`.

## Endpoints implémentés

Namespace `places` (base path `/api/v1/places`)
- POST `/` : créer un lieu
	- Corps JSON requis : `title`, `price`, `latitude`, `longitude`, `owner_id`, `amenities` (liste d'IDs)
	- Validations :
		- `price` : float ≥ 0
		- `latitude` : -90 ≤ latitude ≤ 90
		- `longitude` : -180 ≤ longitude ≤ 180
	- Réponse : objet lieu créé (201) ou erreur 400

- GET `/` : lister tous les lieux (retourne id, title, latitude, longitude)

- GET `/<place_id>` : détails d'un lieu (inclut `owner`, `amenities`, `reviews`)

- PUT `/<place_id>` : mettre à jour un lieu (title, description, price, latitude, longitude)

Namespace `reviews` (base path `/api/v1/reviews`)
- POST `/` : créer un avis
	- Corps JSON requis : `user_id`, `place_id`, `text`
	- Validation : `text` non vide
	- Vérifie que `user_id` et `place_id` existent dans les dépôts en mémoire
	- Réponse : objet review créé (201) ou erreur 400

- GET `/` : lister tous les avis
- GET `/<review_id>` : récupérer un avis
- PUT `/<review_id>` : mettre à jour un avis
- DELETE `/<review_id>` : supprimer un avis

## Tests rapides

Créer un review:

```powershell
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ -H "Content-Type: application/json" -d '{"user_id":"<user-id>","place_id":"<place-id>","text":"Super séjour"}'
```

Créer un place :

```powershell
curl -X POST http://127.0.0.1:5000/api/v1/places/ -H "Content-Type: application/json" -d '{"title":"Cozy","description":"Nice","price":100.0,"latitude":37.7,"longitude":-122.4,"owner_id":"<owner-id>","amenities":["<amenity-id>"]}'
```
