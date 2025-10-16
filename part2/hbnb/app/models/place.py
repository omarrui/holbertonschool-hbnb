from app.models.base import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self._price = None
        self._latitude = None
        self._longitude = None
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        try:
            val = float(value)
        except (TypeError, ValueError):
            raise ValueError('price must be a number')
        if val < 0:
            raise ValueError('price must be non-negative')
        self._price = val

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        try:
            val = float(value)
        except (TypeError, ValueError):
            raise ValueError('latitude must be a number')
        if val < -90 or val > 90:
            raise ValueError('latitude must be between -90 and 90')
        self._latitude = val

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        try:
            val = float(value)
        except (TypeError, ValueError):
            raise ValueError('longitude must be a number')
        if val < -180 or val > 180:
            raise ValueError('longitude must be between -180 and 180')
        self._longitude = val

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def to_dict(self):
        """Serialize place to a dict suitable for API responses."""
        return {
            'id': self.id,
            'title': getattr(self, 'title', None),
            'description': getattr(self, 'description', None),
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': getattr(self, 'owner', None),
            'amenities': [a.id if hasattr(a, 'id') else a for a in self.amenities],
            'created_at': getattr(self, 'created_at').isoformat() if hasattr(self, 'created_at') else None,
            'updated_at': getattr(self, 'updated_at').isoformat() if hasattr(self, 'updated_at') else None
        }