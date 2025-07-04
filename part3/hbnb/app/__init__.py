from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.extensions import db, bcrypt, jwt

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Create API
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')
    
    # Import and add namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.protected import api as protected_ns
    
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(protected_ns, path='/api/v1/protected')
    
    # Return the app instance
    return app
