from abc import ABC, abstractmethod
from app.extensions import db  # Fixed import path
from app import db
from app.models.amenity import Amenity

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass

class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
        return obj

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        for obj in self._storage.values():
            if getattr(obj, attr_name, None) == attr_value:
                return obj
        return None

class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
        return obj

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
    
    class AmenityRepository:
        def add(self, amenity):
            """Add a new amenity to the database."""
            db.session.add(amenity)
            db.session.commit()

        def get(self, amenity_id):
            """Retrieve an amenity by its ID."""
            return Amenity.query.get(amenity_id)

        def get_all(self):
            """Retrieve all amenities."""
            return Amenity.query.all()

        def update(self, amenity_id, data):
            """Update an amenity's attributes."""
            amenity = self.get(amenity_id)
            if amenity:
                for key, value in data.items():
                    setattr(amenity, key, value)
                db.session.commit()

        def delete(self, amenity_id):
            """Delete an amenity by its ID."""
            amenity = self.get(amenity_id)
            if amenity:
                db.session.delete(amenity)
                db.session.commit()