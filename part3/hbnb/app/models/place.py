from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository


class HBnBFacade:
    """
    Facade for managing Users, Places, Reviews, and Amenities using SQLAlchemy repositories.
    Relationships are not implemented yet (Task 8).
    """

    def __init__(self):
        # SQLAlchemy repositories for all entities
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # ----------------- User Methods ----------------- #
    def create_user(self, data: dict):
        user = User(**data)
        if "password" in data:
            user.hash_password(data["password"])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str):
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
        self.user_repo.update(user_id, data)
        return user

    def delete_user(self, user_id: str):
        return self.user_repo.delete(user_id)

    # ----------------- Place Methods ----------------- #
    def create_place(self, data: dict):
        place = Place(**data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id: str):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id: str, data: dict):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        place.update(data)
        self.place_repo.update(place_id, data)
        return place

    def delete_place(self, place_id: str):
        return self.place_repo.delete(place_id)

    # ----------------- Review Methods ----------------- #
    def create_review(self, data: dict):
        review = Review(**data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id: str):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id: str, data: dict):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        review.update(data)
        self.review_repo.update(review_id, data)
        return review

    def delete_review(self, review_id: str):
        return self.review_repo.delete(review_id)

    # ----------------- Amenity Methods ----------------- #
    def create_amenity(self, data: dict):
        amenity = Amenity(**data)
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
        self.amenity_repo.update(amenity_id, data)
        return amenity

    def delete_amenity(self, amenity_id: str):
        return self.amenity_repo.delete(amenity_id)
