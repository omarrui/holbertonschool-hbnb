from datetime import datetime
from app.extensions import db
import uuid

class BaseModel(db.Model):
    __abstract__ = True
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def save(self):
        """Save the current instance to the database."""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Update instance attributes with provided data."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def delete(self):
        """Delete the current instance from the database."""
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """Convert instance to dictionary."""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }