from flask import Flask
from flask_restx import Api
from app.extensions import db, bcrypt, jwt

def create_app(config_class="config.DevelopmentConfig"):
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
    api.add_namespace(users_ns, path='/api/v1/users')
    
    # Create database tables
    with app.app_context():
        db.create_all()

    return app
