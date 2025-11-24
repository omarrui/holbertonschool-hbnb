from app import db
from app.persistence.repository import Repository  # make sure this path matches your project structure

class SQLAlchemyRepository(Repository):
    """A repository that uses SQLAlchemy for persistence."""

    def __init__(self, model):
        self.model = model

    def add(self, obj):
        """Add a new object to the database."""
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """Retrieve an object by its ID."""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Retrieve all objects of this model."""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Update an existing object by ID."""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        """Delete an object by its ID."""
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """Find an object using a specific attribute."""
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
