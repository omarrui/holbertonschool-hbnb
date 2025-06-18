from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Import and add namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    # Add more namespaces as you implement them

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')

    return app
