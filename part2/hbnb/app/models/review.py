from app.models.base import BaseModel


class Review(BaseModel):
    def __init__(self, user_id, place_id, text):
        super().__init__()
        self.user_id = user_id
        self.place_id = place_id
        self.text = None
        self.text = text  # validate via setter

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

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'text': self.text
        }
