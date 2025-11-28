import uuid
from datetime import datetime
from app import db


class BaseModel(db.Model):
    """Base model for all database models."""
    
    __abstract__ = True  # ← SQLAlchemy ne créera pas de table pour cette classe
    
    # Colonnes communes à tous les modèles
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def save(self):
        """Save to database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete from database."""
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        """Update attributes from dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        self.save()

    def to_dict(self):
        """Convert to dictionary."""
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, datetime):
                    result[key] = value.isoformat()
                else:
                    result[key] = value
        return result