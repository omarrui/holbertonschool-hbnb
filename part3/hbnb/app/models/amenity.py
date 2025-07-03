#!/usr/bin/env python3
"""Model for amenities"""

from app.models.base import BaseModel
from app.extensions import db


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, name):
        super().__init__()
        self.name = name

    def validate(self):
        """Validate the Amenity attributes."""
        if not isinstance(self.name, str) or len(self.name.strip()) == 0:
            raise ValueError("Amenity name must be a non-empty string.")

        if len(self.name) > 100:
            raise ValueError("Amenity name must be ≤ 100 characters.")

        return True
