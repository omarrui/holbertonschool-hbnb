"""Register all models for SQLAlchemy metadata before create_all."""
from .base_model import BaseModel  # noqa: F401
from .user import User  # noqa: F401
from .amenity import Amenity  # noqa: F401
from .place import Place, place_amenity  # noqa: F401
from .review import Review  # noqa: F401
