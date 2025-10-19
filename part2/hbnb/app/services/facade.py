from app.persistence.repository import InMemoryRepository
from app.models.place import Place
from app.models.review import Review
from app.models.user import User


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ---------------- Users ----------------
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.update(user_data)
        return user

    # ---------------- Amenities ----------------
    def create_amenity(self, amenity_data):
        from app.models.amenity import Amenity

        name = amenity_data.get('name')
        if not name:
            raise ValueError('name is required')

        amen = Amenity(name)
        self.amenity_repo.add(amen)
        return amen

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amen = self.amenity_repo.get(amenity_id)
        if not amen:
            return None
        amen.update(amenity_data)
        return amen

    # ---------------- Places ----------------
    def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError('owner not found')

        amenities_ids = place_data.get('amenities', [])
        amenities_objs = []
        for a_id in amenities_ids:
            amen = self.amenity_repo.get(a_id)
            if not amen:
                raise ValueError(f'amenity {a_id} not found')
            amenities_objs.append(amen)

        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description'),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner=owner_id,
        )

        for amen in amenities_objs:
            place.add_amenity(amen)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        owner = self.user_repo.get(place.owner)

        amenities = []
        for a in getattr(place, 'amenities', []):
            amen_obj = a if hasattr(a, 'id') else self.amenity_repo.get(a)
            if amen_obj:
                amenities.append(amen_obj)

        reviews = []
        for r in getattr(place, 'reviews', []):
            reviews.append(r)

        return {'place': place, 'owner': owner, 'amenities': amenities, 'reviews': reviews}

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        updatable = {}
        for key in ('title', 'description', 'price', 'latitude', 'longitude'):
            if key in place_data:
                updatable[key] = place_data[key]

        place.update(updatable)
        return place

    # Reviews
    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        text = review_data.get('text')

        if not user_id or not self.user_repo.get(user_id):
            raise ValueError('user not found')
        if not place_id or not self.place_repo.get(place_id):
            raise ValueError('place not found')
        if not text:
            raise ValueError('text is required')

        review = Review(user_id=user_id, place_id=place_id, text=text)
        self.review_repo.add(review)

        place = self.place_repo.get(place_id)
        if place:
            place.add_review(review)

        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return getattr(place, 'reviews', [])

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        if 'text' in review_data:
            review.text = review_data['text']
        review.save()
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False

        place = self.place_repo.get(review.place_id)
        if place and hasattr(place, 'reviews'):
            place.reviews = [r for r in place.reviews if r.id != review_id]

        self.review_repo.delete(review_id)
        return True
"""HBnBFacade

Single, clean facade implementation used by the API. This file provides the
business logic required by the tests: creating/updating/getting users,
amenities, places and reviews. It intentionally validates relations (owner,
amenities, user/place for reviews) and relies on model-level validation for
fields such as price/latitude/longitude and review text.
"""

from app.persistence.repository import InMemoryRepository
from app.models.place import Place
from app.models.review import Review
from app.models.user import User


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ---------------- Users ----------------
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.update(user_data)
        return user

    # ---------------- Amenities ----------------
    def create_amenity(self, amenity_data):
        from app.models.amenity import Amenity

        name = amenity_data.get('name')
        if not name:
            raise ValueError('name is required')

        amen = Amenity(name)
        self.amenity_repo.add(amen)
        return amen

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amen = self.amenity_repo.get(amenity_id)
        if not amen:
            return None
        amen.update(amenity_data)
        return amen

    # ---------------- Places ----------------
    def create_place(self, place_data):
        # Validate owner exists
        owner_id = place_data.get('owner_id')
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError('owner not found')

        # Validate amenities exist and collect amenity objects
        amenities_ids = place_data.get('amenities', [])
        amenities_objs = []
        for a_id in amenities_ids:
            amen = self.amenity_repo.get(a_id)
            if not amen:
                raise ValueError(f'amenity {a_id} not found')
            amenities_objs.append(amen)

        # Create Place instance (Place will validate price/lat/lon)
        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description'),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner=owner_id,
        )

        # Attach amenities
        for amen in amenities_objs:
            place.add_amenity(amen)

        # Persist
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        owner = self.user_repo.get(place.owner)

        amenities = []
        for a in getattr(place, 'amenities', []):
            amen_obj = a if hasattr(a, 'id') else self.amenity_repo.get(a)
            if amen_obj:
                amenities.append(amen_obj)

        reviews = []
        for r in getattr(place, 'reviews', []):
            reviews.append(r)

        return {'place': place, 'owner': owner, 'amenities': amenities, 'reviews': reviews}

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        updatable = {}
        for key in ('title', 'description', 'price', 'latitude', 'longitude'):
            if key in place_data:
                updatable[key] = place_data[key]

        place.update(updatable)
        return place

    # ---------------- Reviews ----------------
    def create_review(self, review_data):
        # Validate user and place exist
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        text = review_data.get('text')

        if not user_id or not self.user_repo.get(user_id):
            raise ValueError('user not found')
        if not place_id or not self.place_repo.get(place_id):
            raise ValueError('place not found')
        if not text:
            raise ValueError('text is required')

        review = Review(user_id=user_id, place_id=place_id, text=text)
        self.review_repo.add(review)

        place = self.place_repo.get(place_id)
        if place:
            place.add_review(review)

        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return getattr(place, 'reviews', [])

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        if 'text' in review_data:
            review.text = review_data['text']
        review.save()
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False

        place = self.place_repo.get(review.place_id)
        if place and hasattr(place, 'reviews'):
            place.reviews = [r for r in place.reviews if r.id != review_id]

        self.review_repo.delete(review_id)
        return True
from app.models.place import Place
from app.models.review import Review
from app.models.user import User


class HBnBFacade:
    """Single clean facade used by the API."""

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Users
    def create_user(self, data):
        user = User(**data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.update(data)
        return user

    # Amenities
    def create_amenity(self, data):
        from app.models.amenity import Amenity
        name = data.get('name')
        if not name:
            raise ValueError('name is required')
        amen = Amenity(name)
        self.amenity_repo.add(amen)
        return amen

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        amen = self.amenity_repo.get(amenity_id)
        if not amen:
            return None
        amen.update(data)
        return amen

    # Places
    def create_place(self, data):
        owner_id = data.get('owner_id')
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError('owner not found')

        amenities_ids = data.get('amenities', [])
        for a_id in amenities_ids:
            if not self.amenity_repo.get(a_id):
                raise ValueError(f'amenity {a_id} not found')

        place = Place(
            title=data.get('title'),
            description=data.get('description'),
            price=data.get('price'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            owner=owner_id,
        )
        place.amenities = amenities_ids
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        owner = self.user_repo.get(place.owner)
        amenities = [self.amenity_repo.get(a_id) for a_id in getattr(place, 'amenities', []) if self.amenity_repo.get(a_id)]
        reviews = getattr(place, 'reviews', [])
        return {'place': place, 'owner': owner, 'amenities': amenities, 'reviews': reviews}

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        updatable = {}
        for key in ('title', 'description', 'price', 'latitude', 'longitude'):
            if key in data:
                updatable[key] = data[key]
        place.update(updatable)
        return place

    # Reviews
    def create_review(self, data):
        user_id = data.get('user_id')
        place_id = data.get('place_id')
        if not user_id or not self.user_repo.get(user_id):
            raise ValueError('user not found')
        if not place_id or not self.place_repo.get(place_id):
            raise ValueError('place not found')
        review = Review(user_id=user_id, place_id=place_id, text=data.get('text'))
        self.review_repo.add(review)
        place = self.place_repo.get(place_id)
        if place:
            if not hasattr(place, 'reviews'):
                place.reviews = []
            place.reviews.append(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return getattr(place, 'reviews', [])

    def update_review(self, review_id, data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        if 'text' in data:
            review.text = data['text']
        review.save()
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        place = self.place_repo.get(review.place_id)
        if place and hasattr(place, 'reviews'):
            place.reviews = [r for r in place.reviews if r.id != review_id]
        self.review_repo.delete(review_id)
        return True
from app.persistence.repository import InMemoryRepository
from app.models.place import Place
from app.models.review import Review
from app.models.user import User


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Users
    def create_user(self, data):
        user = User(**data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.update(data)
        return user

    # Amenities
    def create_amenity(self, data):
        from app.models.amenity import Amenity

        name = data.get('name')
        if not name:
            raise ValueError('name is required')
        amen = Amenity(name)
        self.amenity_repo.add(amen)
        return amen

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        amen = self.amenity_repo.get(amenity_id)
        if not amen:
            return None
        amen.update(data)
        return amen

    # Places
    def create_place(self, data):
        owner_id = data.get('owner_id')
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError('owner not found')

        amenities_ids = data.get('amenities', [])
        for a_id in amenities_ids:
            if not self.amenity_repo.get(a_id):
                raise ValueError(f'amenity {a_id} not found')

        place = Place(
            title=data.get('title'),
            description=data.get('description'),
            price=data.get('price'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            owner=owner_id,
        )

        place.amenities = amenities_ids
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        owner = self.user_repo.get(place.owner)
        amenities = [self.amenity_repo.get(a_id) for a_id in getattr(place, 'amenities', []) if self.amenity_repo.get(a_id)]
        reviews = getattr(place, 'reviews', [])
        return {'place': place, 'owner': owner, 'amenities': amenities, 'reviews': reviews}

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        updatable = {}
        for key in ('title', 'description', 'price', 'latitude', 'longitude'):
            if key in data:
                updatable[key] = data[key]
        place.update(updatable)
        return place

    # Reviews
    def create_review(self, data):
        user_id = data.get('user_id')
        place_id = data.get('place_id')
        if not user_id or not self.user_repo.get(user_id):
            raise ValueError('user not found')
        if not place_id or not self.place_repo.get(place_id):
            raise ValueError('place not found')
        review = Review(user_id=user_id, place_id=place_id, text=data.get('text'))
        self.review_repo.add(review)
        place = self.place_repo.get(place_id)
        if place:
            if not hasattr(place, 'reviews'):
                place.reviews = []
            place.reviews.append(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return getattr(place, 'reviews', [])

    def update_review(self, review_id, data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        if 'text' in data:
            review.text = data['text']
        review.save()
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        place = self.place_repo.get(review.place_id)
        if place and hasattr(place, 'reviews'):
            place.reviews = [r for r in place.reviews if r.id != review_id]
        self.review_repo.delete(review_id)
        return True
from app.persistence.repository import InMemoryRepository
from app.models.place import Place
from app.models.review import Review
from app.models.user import User


class HBnBFacade:
    """Facade providing business operations over in-memory repositories.

    Provides create/get/update operations for Users, Amenities, Places and Reviews
    used by the API layer.
    """

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ---------------- Users ----------------
    def create_user(self, data):
        user = User(**data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.update(data)
        return user

    # ---------------- Amenities ----------------
    def create_amenity(self, data):
        from app.models.amenity import Amenity

        name = data.get('name')
        if not name:
            raise ValueError('name is required')

        amen = Amenity(name)
        self.amenity_repo.add(amen)
        return amen

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        amen = self.amenity_repo.get(amenity_id)
        if not amen:
            return None
        amen.update(data)
        return amen

    # ---------------- Places ----------------
    def create_place(self, data):
        owner_id = data.get('owner_id')
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError('owner not found')

        amenities_ids = data.get('amenities', [])
        amenities_objs = []
        for a_id in amenities_ids:
            amen = self.amenity_repo.get(a_id)
            if not amen:
                raise ValueError(f'amenity {a_id} not found')
            amenities_objs.append(amen)

        place = Place(
            title=data.get('title'),
            description=data.get('description'),
            price=data.get('price'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            owner=owner_id,
        )

        for amen in amenities_objs:
            place.add_amenity(amen)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        owner = self.user_repo.get(place.owner)

        amenities = []
        for a in getattr(place, 'amenities', []):
            amen_obj = a if hasattr(a, 'id') else self.amenity_repo.get(a)
            if amen_obj:
                amenities.append(amen_obj)

        reviews = []
        for r in getattr(place, 'reviews', []):
            reviews.append(r)

        return {'place': place, 'owner': owner, 'amenities': amenities, 'reviews': reviews}

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        updatable = {}
        for key in ('title', 'description', 'price', 'latitude', 'longitude'):
            if key in data:
                updatable[key] = data[key]

        place.update(updatable)
        return place

    # ---------------- Reviews ----------------
    def create_review(self, data):
        user_id = data.get('user_id')
        place_id = data.get('place_id')
        text = data.get('text')

        if not user_id or not self.user_repo.get(user_id):
            raise ValueError('user not found')
        if not place_id or not self.place_repo.get(place_id):
            raise ValueError('place not found')

        review = Review(user_id=user_id, place_id=place_id, text=text)
        self.review_repo.add(review)

        place = self.place_repo.get(place_id)
        if place:
            place.add_review(review)

        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return getattr(place, 'reviews', [])

    def update_review(self, review_id, data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        if 'text' in data:
            review.text = data['text']
        review.save()
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False

        place = self.place_repo.get(review.place_id)
        if place and hasattr(place, 'reviews'):
            place.reviews = [r for r in place.reviews if r.id != review_id]

        self.review_repo.delete(review_id)
        return True
from app.persistence.repository import InMemoryRepository
from app.models.place import Place
from app.models.review import Review
from app.models.user import User


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # -------------------- Users --------------------
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if user:
            user.update(user_data)
            self.user_repo.update(user_id, user)
        return user

    # -------------------- Amenities --------------------
    def create_amenity(self, amenity_data):
        from app.models.amenity import Amenity
        name = amenity_data.get('name')
        if not name:
            raise ValueError('name is required')
        amen = Amenity(name)
        self.amenity_repo.add(amen)
        return amen

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amen = self.amenity_repo.get(amenity_id)
        if not amen:
            return None
        amen.update(amenity_data)
        return amen

    # -------------------- Places --------------------
    def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError('owner not found')

        amenities_ids = place_data.get('amenities', [])
        amenities_objs = []
        for a_id in amenities_ids:
            amen = self.amenity_repo.get(a_id)
            if not amen:
                raise ValueError(f'amenity {a_id} not found')
            amenities_objs.append(amen)

        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description'),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner=owner_id
        )

        for amen in amenities_objs:
            place.add_amenity(amen)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        owner = self.user_repo.get(place.owner)

        amenities = []
        for a in getattr(place, 'amenities', []):
            amen_obj = a if hasattr(a, 'id') else self.amenity_repo.get(a)
            if amen_obj:
                amenities.append(amen_obj)

        reviews = []
        for r in getattr(place, 'reviews', []):
            reviews.append(r)

        return {
            'place': place,
            'owner': owner,
            'amenities': amenities,
            'reviews': reviews
        }

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        updatable = {}
        for key in ('title', 'description', 'price', 'latitude', 'longitude'):
            if key in place_data:
                updatable[key] = place_data[key]

        place.update(updatable)
        return place

    # -------------------- Reviews --------------------
    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        text = review_data.get('text')

        if not user_id or not self.user_repo.get(user_id):
            raise ValueError('user not found')
        if not place_id or not self.place_repo.get(place_id):
            raise ValueError('place not found')

        review = Review(user_id=user_id, place_id=place_id, text=text)
        self.review_repo.add(review)

        place = self.place_repo.get(place_id)
        if place:
            place.add_review(review)

        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return getattr(place, 'reviews', [])

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        if 'text' in review_data:
            review.text = review_data['text']
        review.save()
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False

        place = self.place_repo.get(review.place_id)
        if place and hasattr(place, 'reviews'):
            place.reviews = [r for r in place.reviews if r.id != review_id]

        self.review_repo.delete(review_id)
        return True

        amen = Amenity(name)
        self.amenity_repo.add(amen)
        return amen

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amen = self.amenity_repo.get(amenity_id)
        if not amen:
            return None
        amen.update(amenity_data)
        return amen

    def create_place(self, place_data):
        # Validate owner exists
        owner_id = place_data.get('owner_id')
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError('owner not found')

        # Validate amenities exist and collect amenity objects
        amenities_ids = place_data.get('amenities', [])
        amenities_objs = []
        for a_id in amenities_ids:
            amen = self.amenity_repo.get(a_id)
            if not amen:
                raise ValueError(f'amenity {a_id} not found')
            amenities_objs.append(amen)

        # Create Place instance (Place will validate price/lat/lon)
        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description'),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner=owner_id
        )

        # Attach amenities
        for amen in amenities_objs:
            place.add_amenity(amen)

        # Persist
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # Gather owner details
        owner = self.user_repo.get(place.owner)

        # Gather amenity details
        amenities = []
        for a in getattr(place, 'amenities', []):
            # amenity stored either as object or id
            amen_obj = a if hasattr(a, 'id') else self.amenity_repo.get(a)
            if amen_obj:
                amenities.append(amen_obj)

        # Gather reviews for the place
        reviews = []
        for r in getattr(place, 'reviews', []):
            reviews.append(r)

        return {
            'place': place,
            'owner': owner,
            'amenities': amenities,
            'reviews': reviews
        }

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # Only allow updating certain fields
        updatable = {}
        for key in ('title', 'description', 'price', 'latitude', 'longitude'):
            if key in place_data:
                updatable[key] = place_data[key]

        # Apply simple update via object's update method (which calls save)
        place.update(updatable)

        return place

    def create_review(self, review_data):
        # Validate user and place exist
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        text = review_data.get('text')

        if not user_id or not self.user_repo.get(user_id):
            raise ValueError('user not found')
        if not place_id or not self.place_repo.get(place_id):
            raise ValueError('place not found')

        # Create review (Review validates text)
        review = Review(user_id=user_id, place_id=place_id, text=text)

        # Persist
        self.review_repo.add(review)

        # Attach to place object
        place = self.place_repo.get(place_id)
        if place:
            place.add_review(review)

        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        # Return reviews related to a specific place
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return getattr(place, 'reviews', [])

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        # Allow updating text only
        if 'text' in review_data:
            review.text = review_data['text']
        review.save()
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False

        # Remove from place.reviews if attached
        place = self.place_repo.get(review.place_id)
        if place and hasattr(place, 'reviews'):
            place.reviews = [r for r in place.reviews if r.id != review_id]

        # Delete from repo
        self.review_repo.delete(review_id)
        return True

    def create_amenity(self, amenity_data):
        # Placeholder for logic to create an amenity
        pass

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amen = self.amenity_repo.get(amenity_id)
        if not amen:
            return None
        amen.update(amenity_data)
        return amen
