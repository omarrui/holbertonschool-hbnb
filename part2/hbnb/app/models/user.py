from app.models.base import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': getattr(self, 'first_name', None),
            'last_name': getattr(self, 'last_name', None),
            'email': getattr(self, 'email', None)
        }
