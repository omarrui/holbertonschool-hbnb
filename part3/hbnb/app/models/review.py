from app.models.base import BaseModel

class Review(BaseModel):
    def __init__(self, user_id: str, place_id: str, text: str, rating: int):
        super().__init__()
        self.user_id = user_id
        self.place_id = place_id
        self.text = text
        self.rating = rating

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("text is required")
        self._text = value.strip()

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if isinstance(value, bool):
            raise ValueError("rating must be an integer between 1 and 5")
        try:
            iv = int(value)
        except (TypeError, ValueError):
            raise ValueError("rating must be an integer between 1 and 5")
        if iv < 1 or iv > 5:
            raise ValueError("rating must be an integer between 1 and 5")
        self._rating = iv

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "text": self.text,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
