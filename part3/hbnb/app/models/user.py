import re
from app.models.base import BaseModel
from app.extensions import db, bcrypt

class User(BaseModel):
    __tablename__ = 'users'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        if password:
            self.hash_password(password)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def is_valid_email(email):
        """Validates email format."""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    def to_dict(self, include_password=False):
        """Convert user to dictionary, excluding password by default."""
        user_dict = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_password and self.password:
            user_dict['password'] = self.password
            
        return user_dict

    def checking(self):
        """Validate user data."""
        if not self.first_name or len(self.first_name.strip()) == 0:
            raise ValueError("First name is required")
        
        if not self.last_name or len(self.last_name.strip()) == 0:
            raise ValueError("Last name is required")
        
        if not self.email or not self.is_valid_email(self.email):
            raise ValueError("Valid email is required")
        
        if len(self.first_name) > 50:
            raise ValueError("First name must be 50 characters or less")
        
        if len(self.last_name) > 50:
            raise ValueError("Last name must be 50 characters or less")

        return True