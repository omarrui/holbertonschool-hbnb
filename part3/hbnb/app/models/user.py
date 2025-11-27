from app import db, bcrypt
from app.models.base_model import BaseModel
from sqlalchemy.ext.hybrid import hybrid_property
import re

class User(BaseModel):
    __tablename__ = 'users'

    _first_name = db.Column("first_name", db.String(50), nullable=False)
    _last_name = db.Column("last_name", db.String(50), nullable=False)
    _email = db.Column("email", db.String(120), unique=True, nullable=False)
    _password = db.Column("password", db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', backref='owner', lazy=True, cascade="all, delete-orphan")
    reviews = db.relationship('Review', backref='user', lazy=True, cascade="all, delete-orphan")


    @hybrid_property
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
    @hybrid_property
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

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if value is None:
            raise ValueError("Invalid email")
        v = value.strip().lower()
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError("Invalid email")
        self._email = v
    @hybrid_property
    def password(self):
        """
        Get the user's password.
        """
        return self._password
    
    @password.setter
    def password(self, value):
        """
        Set the user's password.
        """
        if not value or len(value) < 8:
            raise ValueError('Password must be at least 8 characters.')
        if len(value) > 255:
            raise ValueError('Password must be less than 255 characters.')
        self.hash_password(value)

    def hash_password(self, password):
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }
