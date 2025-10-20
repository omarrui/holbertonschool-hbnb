from .base import BaseModel

class Amenity(BaseModel):
    """Represents an amenity (feature) available in a Place."""

    def __init__(self, name):
        """Initialize a new Amenity instance."""
        super().__init__()
        self.name = name

    @property
    def name(self):
        """Get the amenity name."""
        return self._name

    @name.setter
    def name(self, value):
        """Set the amenity name with validation."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Amenity name is required")
        if len(value) > 50:
            raise ValueError("Amenity name must be less than 50 characters")
        self._name = value.strip()

    def to_dict(self):
        """Serialize the amenity into a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
