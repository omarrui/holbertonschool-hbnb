#!/usr/bin/env python3
"""Review model for HolbertonBnB application."""

from app.models.base_model import BaseModel
# from app import db  # CIRCULAR IMPORT FIX

def _get_db():
    """Import db only when needed to avoid circular import."""
    from app import db
    return db


class Review(BaseModel):
    """Represents a review for a place.

    Attributes:
        text (str): Content of the review.
        rating (int): Rating given (1-5 stars).
        place_id (str): ID of the place being reviewed.
        user_id (str): ID of the user who wrote the review.
    """

    __tablename__ = 'reviews'

    text = _get_db().Column(_get_db().String(), nullable=False)
    rating = _get_db().Column(_get_db().Integer, nullable=False)
    place_id = _get_db().Column(_get_db().String(36), _get_db().ForeignKey('places.id'), nullable=False)
    user_id = _get_db().Column(_get_db().String(36), _get_db().ForeignKey('users.id'), nullable=False)

    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
        
        # Manual validation
        self._validate_text(text)
        self._validate_rating(rating)

    def _validate_text(self, text):
        """Ensure review text is not empty."""
        if not text or not text.strip():
            raise ValueError("Review text cannot be empty.")

    def _validate_rating(self, rating):
        """Ensure rating is between 1 and 5."""
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer.")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")

    def to_dict(self):
        """Return dictionary representation of the review."""
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
