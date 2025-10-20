from app.models.base import BaseModel

class Place(BaseModel):
    """Represents a rental property in the application."""

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        if not owner:
            raise ValueError("Invalid owner")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title cannot be empty")
        if len(value) > 100:
            raise ValueError("Title must be 100 characters max.")
        self._title = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value is None:
            raise ValueError("Price cannot be None")
        try:
            val = float(value)
        except (TypeError, ValueError):
            raise ValueError("Price must be a number")
        if val < 0:
            raise ValueError("Price cannot be negative")
        self._price = val

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if value is None:
            raise ValueError("Latitude cannot be None")
        try:
            val = float(value)
        except (TypeError, ValueError):
            raise ValueError("Latitude must be a valid number")
        if not (-90 <= val <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = val

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if value is None:
            raise ValueError("Longitude cannot be None")
        try:
            val = float(value)
        except (TypeError, ValueError):
            raise ValueError("Longitude must be a valid number")
        if not (-180 <= val <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = val

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": getattr(self, "owner", None),
            "amenities": [a.id if hasattr(a, "id") else a for a in self.amenities],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
