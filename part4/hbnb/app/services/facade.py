from app.persistence.repository import InMemoryRepository, SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """
    Façade pour relier l'API aux dépôts en mémoire.
    """

    def __init__(self):
        try:
            self.user_repo = SQLAlchemyRepository(User)
            self.amenity_repo = SQLAlchemyRepository(Amenity)
            self.place_repo = SQLAlchemyRepository(Place)
            self.review_repo = SQLAlchemyRepository(Review)
        except Exception:
            self.user_repo = InMemoryRepository()
            self.amenity_repo = InMemoryRepository()
            self.place_repo = InMemoryRepository()
            self.review_repo = InMemoryRepository()


    def create_user(self, user_data):
        # Separate password from other fields to respect User.__init__ signature
        pwd = user_data.pop('password', None)
        allowed = {k: user_data[k] for k in ['first_name', 'last_name', 'email'] if k in user_data}
        if len(allowed) < 3:
            raise ValueError('first_name, last_name and email are required')
        user = User(**allowed)
        if pwd:
            user.set_password(pwd)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email: str):
        return self.user_repo.model.query.filter_by(email=email).first()


    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id: str, data: dict):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.update(data)
        return user

    def create_amenity(self, data: dict):
        from app.models.amenity import Amenity
        name = data.get("name")
        if not name:
            raise ValueError("name is required")
        amenity = Amenity(name=name)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id: str):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id: str, data: dict):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.update(data)
        return amenity

    def create_place(self, data: dict):
        host_id = data.get('host_id') or data.get('owner_id')
        if not host_id or not self.user_repo.get(host_id):
            raise ValueError('host not found')

        name = data.get('name') or data.get('title')
        if name is None or not str(name).strip():
            raise ValueError('name cannot be empty')
        if len(name) > 100:
            raise ValueError('name too long')

        price_per_night = data.get('price_per_night') or data.get('price')
        if price_per_night is not None and price_per_night < 0:
            raise ValueError('invalid price_per_night')

        latitude = data.get('latitude')
        if latitude is not None and not (-90 <= latitude <= 90):
            raise ValueError('invalid latitude')

        longitude = data.get('longitude')
        if longitude is not None and not (-180 <= longitude <= 180):
            raise ValueError('invalid longitude')

        amenity_ids = data.get('amenities', [])
        amenities = []
        for a_id in amenity_ids:
            am = self.amenity_repo.get(a_id)
            if not am:
                raise ValueError(f'amenity {a_id} not found')
            amenities.append(am)

        place = Place(
            name=name,
            description=data.get('description'),
            price_per_night=price_per_night or 0,
            latitude=latitude,
            longitude=longitude,
            host_id=host_id
        )
        place.amenities = amenities
        self.place_repo.add(place)
        return place

    def get_place(self, place_id: str):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        owner = self.user_repo.get(place.host_id)
        # place.amenities relationship already returns objects
        amenities = list(getattr(place, 'amenities', []))
        reviews = list(getattr(place, 'reviews', []))
        return {"place": place, "owner": owner, "amenities": amenities, "reviews": reviews}

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id: str, data: dict):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        if 'name' in data:
            name = data['name']
            if name is None or not str(name).strip():
                raise ValueError('name cannot be empty')
            if len(name) > 100:
                raise ValueError('name too long')
            place.name = name

        if 'description' in data:
            place.description = data['description']

        if 'price_per_night' in data:
            ppn = data['price_per_night']
            if ppn is not None and ppn < 0:
                raise ValueError('invalid price_per_night')
            place.price_per_night = ppn

        if 'latitude' in data:
            lat = data['latitude']
            if lat is not None and not (-90 <= lat <= 90):
                raise ValueError('invalid latitude')
            place.latitude = lat

        if 'longitude' in data:
            lon = data['longitude']
            if lon is not None and not (-180 <= lon <= 180):
                raise ValueError('invalid longitude')
            place.longitude = lon

        if 'host_id' in data or 'owner_id' in data:
            new_host = data.get('host_id') or data.get('owner_id')
            if not new_host or not self.user_repo.get(new_host):
                raise ValueError('invalid host_id')
            place.host_id = new_host

        if 'amenities' in data:
            new_ids = data.get('amenities') or []
            new_objs = []
            for a_id in new_ids:
                am = self.amenity_repo.get(a_id)
                if not am:
                    raise ValueError(f'amenity {a_id} not found')
                new_objs.append(am)
            place.amenities = new_objs

        if hasattr(place, 'save'):
            place.save()
        else:
            # SQLAlchemy session commit via repository update pattern
            self.place_repo.db.session.commit()
        return place

    def create_review(self, data: dict):
        """Créer une nouvelle review avec validation stricte."""
        user_id = data.get("user_id")
        place_id = data.get("place_id")
        comment = data.get("comment") or data.get('text')
        rating = data.get("rating")

        if not user_id or not self.user_repo.get(user_id):
            raise ValueError("user not found")
        if not place_id or not self.place_repo.get(place_id):
            raise ValueError("place not found")

        # Comment devient optionnel: stocker chaîne vide si absent / vide
        if comment is None:
            comment = ''
        # Si juste des espaces, normaliser en chaîne vide
        if not str(comment).strip():
            comment = ''

        if rating is None:
            raise ValueError("rating is required")
        try:
            val = int(rating)
        except (TypeError, ValueError):
            raise ValueError("rating must be an integer between 1 and 5")
        if val < 1 or val > 5:
            raise ValueError("rating must be between 1 and 5")

        review = Review(
            comment=comment.strip(),
            rating=val,
            place_id=place_id,
            user_id=user_id
        )
        self.review_repo.add(review)

        # Relationship will link review to place automatically via FK; no manual list mgmt needed for SQLAlchemy.

        return review

    def get_review(self, review_id: str):
        """Récupérer une review par ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Lister toutes les reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id: str):
        """Lister les reviews pour une place donnée."""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return getattr(place, "reviews", [])

    def update_review(self, review_id: str, data: dict):
        """Mettre à jour une review (text et/ou rating)."""
        review = self.review_repo.get(review_id)
        if not review:
            return None

        if 'comment' in data or 'text' in data:
            new_comment = data.get('comment') or data.get('text')
            if new_comment is None:
                # Autoriser effacement du commentaire -> chaîne vide
                review.comment = ''
            else:
                stripped = str(new_comment).strip()
                review.comment = stripped  # peut être vide

        if "rating" in data:
            new_rating = data["rating"]
            try:
                val = int(new_rating)
            except (TypeError, ValueError):
                raise ValueError("rating must be an integer between 1 and 5")
            if val < 1 or val > 5:
                raise ValueError("rating must be between 1 and 5")
            review.rating = val

        if hasattr(review, "save"):
            review.save()

        return review

    def delete_review(self, review_id: str):
        """Supprimer une review existante."""
        review = self.review_repo.get(review_id)
        if not review:
            return False

        place = self.place_repo.get(review.place_id)
        if place and hasattr(place, "reviews"):
            place.reviews = [r for r in place.reviews if r.id != review_id]

        self.review_repo.delete(review_id)
        return True

    def delete_place(self, place_id: str):
        """Supprimer une place (utilisé par endpoint admin)."""
        place = self.place_repo.get(place_id)
        if not place:
            return False
        # Supprimer d'abord les reviews liées (cascade si configuré, sinon manuel)
        reviews = list(getattr(place, 'reviews', []))
        for r in reviews:
            try:
                self.review_repo.delete(r.id)
            except Exception:
                pass
        try:
            self.place_repo.delete(place_id)
        except Exception:
            return False
        return True
