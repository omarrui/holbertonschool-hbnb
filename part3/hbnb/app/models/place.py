from app.models.base_model import BaseModel
# from app import db, bcrypt  # CIRCULAR IMPORT FIX

def _get_db():
    """Import db only when needed to avoid circular import."""
    from app import db
    return db

# Association table for Place-Amenity many-to-many relationship
place_amenity = db.Table('place_amenity',
    _get_db().Column('place_id', _get_db().String(60), _get_db().ForeignKey('places.id'), primary_key=True),
    _get_db().Column('amenity_id', _get_db().String(60), _get_db().ForeignKey('amenities.id'), primary_key=True)
)

class User(BaseModel):
    """Represents a user in the HolbertonBnB application."""

    __tablename__ = 'users'

    # ----------------- Columns ----------------- #
    first_name = _get_db().Column(_get_db().String(50), nullable=False)
    last_name = _get_db().Column(_get_db().String(50), nullable=False)
    email = _get_db().Column(_get_db().String(120), nullable=False, unique=True)
    password = _get_db().Column(_get_db().String(128), nullable=False)
    is_admin = _get_db().Column(_get_db().Boolean, default=False)

    # ----------------- Relationships ----------------- #
    places = _get_db().relationship('Place', backref='owner', lazy=True)
    reviews = _get_db().relationship('Review', backref='user', lazy=True)

    # ----------------- Initialization ----------------- #
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = bool(is_admin)

    # ----------------- Password Methods ----------------- #
    def hash_password(self, password):
        """Hash the password for secure storage."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    # ----------------- Property Validation ----------------- #
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        value = (value or "").strip()
        if not (1 <= len(value) <= 50):
            raise ValueError("First name must be 1-50 characters long")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        value = (value or "").strip()
        if not (1 <= len(value) <= 50):
            raise ValueError("Last name must be 1-50 characters long")
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        value = (value or "").strip().lower()
        if "@" not in value or "." not in value or " " in value:
            raise ValueError("Invalid email format")
        self._email = value

    # ----------------- Serialization ----------------- #
    def to_dict(self):
        """Return dictionary representation of the user."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "places": [place.id for place in self.places],
            "reviews": [review.id for review in self.reviews],
        }

class Place(BaseModel):
    """Represents a place in the HolbertonBnB application."""

    __tablename__ = 'places'

    # ----------------- Columns ----------------- #
    title = _get_db().Column(_get_db().String(100), nullable=False)
    description = _get_db().Column(db.Text, nullable=True)
    price = _get_db().Column(_get_db().Float, nullable=False)
    latitude = _get_db().Column(_get_db().Float, nullable=True)
    longitude = _get_db().Column(_get_db().Float, nullable=True)
    owner_id = _get_db().Column(_get_db().String(60), _get_db().ForeignKey('users.id'), nullable=False)

    # ----------------- Relationships ----------------- #
    reviews = _get_db().relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    amenities = _get_db().relationship('Amenity', secondary=place_amenity, back_populates='places')

    # ----------------- Initialization ----------------- #
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner

    # ----------------- Serialization ----------------- #
    def to_dict(self):
        """Return dictionary representation of the place."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenities": [amenity.id for amenity in self.amenities],
            "reviews": [review.id for review in self.reviews],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
