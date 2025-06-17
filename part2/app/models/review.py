from app.models.base import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place  # Place instance
        self.user = user    # User instance

    def checking(self):
        if not self.text or not isinstance(self.text, str):
            raise ValueError("Text is required and must be a string")
        if self.rating is None or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        if not self.place:
            raise ValueError("Place is required")
        if not self.user:
            raise ValueError("User is required")
