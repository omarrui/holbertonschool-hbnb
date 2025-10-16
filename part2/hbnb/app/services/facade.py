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

    # User methods
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

    def create_amenity(self, amenity_data):
        # Placeholder for logic to create an amenity
        pass

    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        pass

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        pass

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        pass

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
        # Placeholder for logic to retrieve an amenity by ID
        pass

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        pass

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        pass
