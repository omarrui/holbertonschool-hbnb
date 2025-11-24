from app.models.base_model import BaseModel
from app.extensions import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(128), nullable=False, unique=True)
    # Relationship back to places (many-to-many)
    places = db.relationship('Place', secondary='place_amenity', back_populates='amenities')

    def to_dict(self):
        return super().to_dict()
