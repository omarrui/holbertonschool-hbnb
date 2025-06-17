from app.models.base import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner  # User instance
        self.reviews = []
        self.amenities = []

    def checking(self):
        if not self.title or len(self.title) > 100:
            raise ValueError("Title is required and must be <= 100 characters")
        if self.price is None or self.price < 0:
            raise ValueError("Price must be a positive value")
        if self.latitude is None or not (-90.0 <= self.latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")
        if self.longitude is None or not (-180.0 <= self.longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")
        if not self.owner:
            raise ValueError("Owner is required")

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)
