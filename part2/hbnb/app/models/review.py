from app.models.base import BaseModel


class Review(BaseModel):
    def __init__(self, user_id, place_id, text, rating=None):
        super().__init__()
        self.user_id = user_id
        self.place_id = place_id
        self._text = None
        self.text = text  # validate via setter
        self._rating = None
        # rating is optional on creation but will be validated if provided
        if rating is not None:
            self.rating = rating

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if value is None:
            raise ValueError('text is required')
        if not isinstance(value, str):
            raise ValueError('text must be a string')
        if value.strip() == '':
            raise ValueError('text must not be empty')
        self._text = value.strip()

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        try:
            val = int(value)
        except (TypeError, ValueError):
            raise ValueError('rating must be an integer between 1 and 5')
        if val < 1 or val > 5:
            raise ValueError('rating must be between 1 and 5')
        self._rating = val

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'text': self.text,
            'rating': self.rating
        }
