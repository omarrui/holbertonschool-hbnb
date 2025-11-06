# filepath: app/models/base_model.py
import uuid
from datetime import datetime

def _get_db():
    """Import db only when needed to avoid circular import."""
    from app import db
    return db

# Create BaseModel that will inherit from db.Model via late binding
class BaseModel:
    """Base model with common attributes and methods."""
    __abstract__ = True 
    
    def __init_subclass__(cls, **kwargs):
        """Configure subclasses to properly inherit from db.Model"""
        super().__init_subclass__(**kwargs)
        # This will be handled when the class is actually used
        
    def __new__(cls, *args, **kwargs):
        # On first instantiation, ensure we inherit from db.Model
        db = _get_db()
        if not issubclass(cls, db.Model) and cls.__name__ != 'BaseModel':
            # Create a new class that inherits from both BaseModel and db.Model
            cls.__bases__ = (db.Model,) + tuple(base for base in cls.__bases__ if base != BaseModel)
            
            # Add SQLAlchemy columns if not already present
            if not hasattr(cls, 'id'):
                cls.id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
            if not hasattr(cls, 'created_at'):
                cls.created_at = db.Column(db.DateTime, default=datetime.utcnow)
            if not hasattr(cls, 'updated_at'):
                cls.updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        return super().__new__(cls)

    def save(self):
        """Save the current instance to the database."""
        db = _get_db()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the current instance from the database."""
        db = _get_db()
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """Return a dictionary representation of the object."""
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, datetime):
                    result[key] = value.isoformat()
                else:
                    result[key] = value
        return result
