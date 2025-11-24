from app.models.base_model import BaseModel
from app.extensions import db, bcrypt

# Association table for Place-Amenity many-to-many relationship
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(60), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(60), db.ForeignKey('amenities.id'), primary_key=True)
)

from app.models.user import User  # ensure user model loaded separately

class Place(BaseModel):
    """Represents a place in the HolbertonBnB application."""

    __tablename__ = 'places'

    # ----------------- Columns ----------------- #
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price_per_night = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    host_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    image_filename = db.Column(db.String(255), nullable=True)

    # ----------------- Relationships ----------------- #
    host = db.relationship('User', backref='hosted_places', lazy=True)
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenity, back_populates='places')

    # ----------------- Initialization ----------------- #
    def __init__(self, name, description, price_per_night, latitude=None, longitude=None, host_id=None):
        super().__init__()
        self.name = name
        self.description = description
        self.price_per_night = price_per_night
        self.latitude = latitude
        self.longitude = longitude
        if host_id:
            self.host_id = host_id

    # ----------------- Serialization ----------------- #
    def to_dict(self):
        """Return dictionary representation of the place."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price_per_night": self.price_per_night,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "host_id": self.host_id,
            "image_filename": self.image_filename,
            "amenities": [amenity.id for amenity in self.amenities],
            "reviews": [review.id for review in self.reviews],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
