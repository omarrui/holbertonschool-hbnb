from app.models.base import BaseModel
from app import db, bcrypt
import uuid
from .base_model import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = bool(is_admin)

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if value is None:
            raise ValueError("Invalid first name")
        v = value.strip()
        if not v or len(v) > 50:
            raise ValueError("Invalid first name")
        self._first_name = v
    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if value is None:
            raise ValueError("Invalid last name")
        v = value.strip()
        if not v or len(v) > 50:
            raise ValueError("Invalid last name")
        self._last_name = v

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if value is None:
            raise ValueError("Invalid email")
        v = value.strip().lower()
        if (not v) or (' ' in v) or ('@' not in v) or ('.' not in v):
            raise ValueError("Invalid email")
        self._email = v

    def to_dict(self):
        return {
            "id_user": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }
