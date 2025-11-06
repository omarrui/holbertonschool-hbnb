from app.models.base_model import BaseModel
from app import db, bcrypt


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    _password = db.Column('password', db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        if password:
            self.password = password
        else:
            # set a placeholder hashed empty password if not provided
            self._password = bcrypt.generate_password_hash('').decode('utf-8')
        self.is_admin = bool(is_admin)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        if not raw_password or len(raw_password) < 6:
            raise ValueError('Password must be at least 6 characters long')
        self._password = bcrypt.generate_password_hash(raw_password).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self._password, raw_password)

    def hash_password(self, raw_password):
        """Alias used by facade to set the password."""
        self.password = raw_password

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if value is None:
            raise ValueError('Invalid first name')
        v = value.strip()
        if not v or len(v) > 50:
            raise ValueError('Invalid first name')
        self._first_name = v

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if value is None:
            raise ValueError('Invalid last name')
        v = value.strip()
        if not v or len(v) > 50:
            raise ValueError('Invalid last name')
        self._last_name = v

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if value is None:
            raise ValueError('Invalid email')
        v = value.strip().lower()
        if (not v) or (' ' in v) or ('@' not in v) or ('.' not in v):
            raise ValueError('Invalid email')
        self._email = v

    def to_dict(self):

        return {
            'id_user': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
        }
