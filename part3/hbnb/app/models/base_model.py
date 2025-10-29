from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True 

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Save the current instance to the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the current instance from the database."""
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """Return a dictionary representation of the object."""
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
