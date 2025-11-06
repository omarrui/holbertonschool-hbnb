from app.models.user import User
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    """Repository for user-specific queries."""

    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """Find a user by their email address."""
        return self.model.query.filter_by(email=email).first()
