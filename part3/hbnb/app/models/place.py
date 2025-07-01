from app.models.base import BaseModel
from app.extensions import db


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(
            self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = []

    def checking(self):
        if self.price is None or self.price < 0:
            raise ValueError("Le prix doit être un nombre positif.")

        if self.latitude is None or not (-90 <= self.latitude <= 90):
            raise ValueError("La latitude doit être comprise entre -90 et 90.")

        if self.longitude is None or not (-180 <= self.longitude <= 180):
            raise ValueError(
                "La longitude doit être comprise entre -180 et 180."
            )

        if not isinstance(self.description, str) or len(self.description) < 10:
            raise ValueError(
                "La description doit être une chaîne de 10 caractères minimum."
            )

        if not (isinstance(self.owner_id, str) or
                len(self.owner_id.strip()) == 0):
            raise ValueError(
                "L'owner doit être une chaîne de caractères non vide."
            )

        if not isinstance(self.title, str) or len(self.title.strip()) < 3:
            raise ValueError(
                "Le titre doit être une chaîne de 3 caractères minimum."
            )

        return True
