from app.models.base import BaseModel
from app.extensions import db


class Review(BaseModel):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    def validate(self):
        """Validate the Review attributes."""
        if self.text is None or not isinstance(self.text, str) or len(self.text.strip()) == 0:
            raise ValueError("Review text must be a non-empty string.")

        if self.rating is None or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")

        if self.place_id is None or not isinstance(self.place_id, str) or len(self.place_id.strip()) == 0:
            raise ValueError("Place ID must be a non-empty string.")

        if self.user_id is None or not isinstance(self.user_id, str) or len(self.user_id.strip()) == 0:
            raise ValueError("User ID must be a non-empty string.")

        return True
