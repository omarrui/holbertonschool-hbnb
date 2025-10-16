from flask import Flask
from flask_restx import Api
<<<<<<< HEAD
from app.api import users_ns, amenities_ns, places_ns, reviews_ns

=======
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
>>>>>>> origin/main

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Register the namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
<<<<<<< HEAD
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
=======
    
    # Register the amenities namespace
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    
>>>>>>> origin/main
    return app