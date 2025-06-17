from app.models.base import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def checking(self):
        if not self.name or len(self.name) > 50:
            raise ValueError("Amenity name is required and must be <= 50 characters")
