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
        user = User(**user_data)
        if "password" in user_data:
            user.hash_password(user_data["password"])
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
        amenity = Amenity(name)
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
        owner_id = data.get("owner_id")
        if not owner_id or not self.user_repo.get(owner_id):
            raise ValueError("owner not found")

        title = data.get("title")
        if title is None or not str(title).strip():
            raise ValueError("title cannot be empty")
        if len(title) > 100:
            raise ValueError("title too long")

        price = data.get("price")
        if price is not None and price < 0:
            raise ValueError("invalid price")

        latitude = data.get("latitude")
        if latitude is not None and not (-90 <= latitude <= 90):
            raise ValueError("invalid latitude")

        longitude = data.get("longitude")
        if longitude is not None and not (-180 <= longitude <= 180):
            raise ValueError("invalid longitude")

        amenity_ids = data.get("amenities", [])
        for a_id in amenity_ids:
            if not self.amenity_repo.get(a_id):
                raise ValueError(f"amenity {a_id} not found")

        place = Place(
            title=title,
            description=data.get("description"),
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner=owner_id,
        )
        place.amenities = amenity_ids
        place.reviews = []
        self.place_repo.add(place)
        return place

    def get_place(self, place_id: str):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        owner = self.user_repo.get(place.owner)
        amenities = [
            self.amenity_repo.get(aid)
            for aid in getattr(place, "amenities", [])
            if self.amenity_repo.get(aid)
        ]
        reviews = getattr(place, "reviews", [])
        return {"place": place, "owner": owner, "amenities": amenities, "reviews": reviews}

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id: str, data: dict):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        updatable = {}

        if "title" in data:
            title = data["title"]
            if title is None or not str(title).strip():
                raise ValueError("title cannot be empty")
            if len(title) > 100:
                raise ValueError("title too long")
            updatable["title"] = title

        if "description" in data:
            updatable["description"] = data["description"]

        if "price" in data:
            price = data["price"]
            if price is not None and price < 0:
                raise ValueError("invalid price")
            updatable["price"] = price

        if "latitude" in data:
            latitude = data["latitude"]
            if latitude is not None and not (-90 <= latitude <= 90):
                raise ValueError("invalid latitude")
            updatable["latitude"] = latitude

        if "longitude" in data:
            longitude = data["longitude"]
            if longitude is not None and not (-180 <= longitude <= 180):
                raise ValueError("invalid longitude")
            updatable["longitude"] = longitude

        if "owner_id" in data:
            new_owner = data["owner_id"]
            if not new_owner or not self.user_repo.get(new_owner):
                raise ValueError("invalid owner_id")
            place.owner = new_owner

        if "amenities" in data:
            new_ids = data.get("amenities") or []
            for a_id in new_ids:
                if not self.amenity_repo.get(a_id):
                    raise ValueError(f"amenity {a_id} not found")
            place.amenities = new_ids

        if updatable:
            place.update(updatable)

        return place

    def create_review(self, data: dict):
        """Créer une nouvelle review avec validation stricte."""
        user_id = data.get("user_id")
        place_id = data.get("place_id")
        text = data.get("text")
        rating = data.get("rating")

        if not user_id or not self.user_repo.get(user_id):
            raise ValueError("user not found")
        if not place_id or not self.place_repo.get(place_id):
            raise ValueError("place not found")

        if text is None or not str(text).strip():
            raise ValueError("text is required")

        if rating is None:
            raise ValueError("rating is required")
        try:
            val = int(rating)
        except (TypeError, ValueError):
            raise ValueError("rating must be an integer between 1 and 5")
        if val < 1 or val > 5:
            raise ValueError("rating must be between 1 and 5")

        review = Review(
            user_id=user_id,
            place_id=place_id,
            text=text.strip(),
            rating=val
        )
        self.review_repo.add(review)

        place = self.place_repo.get(place_id)
        if not hasattr(place, "reviews"):
            place.reviews = []
        place.reviews.append(review)

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

        if "text" in data:
            new_text = data["text"]
            if new_text is None or not str(new_text).strip():
                raise ValueError("text is required")
            review.text = new_text.strip()

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
