from app.models.base import BaseModel
from app import bcrypt

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
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
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, raw_password):
        if not raw_password or len(raw_password) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        self._password = bcrypt.generate_password_hash(raw_password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self._password, password)
    
    def to_dict(self):
        return {
            "id_user": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }
