from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # User methods
    def create_user(self, user_data):
        """Create a new user with hashed password."""
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email']
        for field in required_fields:
            if field not in user_data or not user_data[field]:
                raise ValueError(f"Missing required field: {field}")

        # Create user instance (password will be hashed in __init__ if provided)
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data.get('password'),
            is_admin=user_data.get('is_admin', False)
        )
        
        # Validate user data
        user.checking()
        
        # Save to repository
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email."""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user."""
        user = self.get_user(user_id)
        if not user:
            return None
        
        # Don't allow password updates through this method
        if 'password' in user_data:
            del user_data['password']
        
        return self.user_repo.update(user_id, user_data)

    # Place methods
    def create_place(self, place_data):
        """Create a new place."""
        place = Place(
            title=place_data['title'],
            description=place_data['description'],
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=place_data['owner_id']
        )
        place.checking()
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place."""
        return self.place_repo.update(place_id, place_data)

    # Amenity methods
    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        amenity = Amenity(name=amenity_data['name'])
        amenity.checking()
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity."""
        return self.amenity_repo.update(amenity_id, amenity_data)

    # Review methods
    def create_review(self, review_data):
        """Create a new review."""
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place_id=review_data['place_id'],
            user_id=review_data['user_id']
        )
        review.checking()
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews."""
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        """Update a review."""
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        """Delete a review."""
        return self.review_repo.delete(review_id)

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place."""
        reviews = self.get_all_reviews()
        return [review for review in reviews if review.place_id == place_id]

    def get_review_by_user_and_place(self, user_id, place_id):
        """Check if a user has already reviewed a place."""
        reviews = self.get_all_reviews()
        for review in reviews:
            if review.user_id == user_id and review.place_id == place_id:
                return review
        return None