from app.models.base_model import BaseModel
from app.extensions import db

class Review(BaseModel):
    __tablename__ = 'reviews'

    # Comment désormais optionnel (nullable=True). Une chaîne vide est aussi acceptée.
    comment = db.Column(db.String, nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, comment, rating, place_id, user_id):
        super().__init__()
        self.comment = comment
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    def to_dict(self):
        return super().to_dict()
