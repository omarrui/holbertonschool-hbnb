from app.models.base_model import BaseModel
from app.extensions import db, bcrypt

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    # Backwards compatibility with earlier method names
    def hash_password(self, password):
        self.set_password(password)

    def verify_password(self, password):
        return self.check_password(password)

    def to_dict(self):
        data = super().to_dict()
        data.pop('password', None)
        data['first_name'] = self.first_name
        data['last_name'] = self.last_name
        data['email'] = self.email
        return data
