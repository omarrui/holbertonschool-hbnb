from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from config import DevelopmentConfig, CONFIG_MAP

bcrypt = Bcrypt()
jwt = JWTManager()


def _resolve_config(config_obj):
    if isinstance(config_obj, type):
        return config_obj
    if isinstance(config_obj, str) and config_obj in CONFIG_MAP:
        return CONFIG_MAP[config_obj]
    if isinstance(config_obj, str) and '.' in config_obj:
        module_path, _, class_name = config_obj.rpartition('.')
        if module_path and class_name:
            mod = __import__(module_path, fromlist=[class_name])
            return getattr(mod, class_name)
    return DevelopmentConfig


def create_app(config_class=DevelopmentConfig):
    config_cls = _resolve_config(config_class)
    app = Flask(__name__)
    app.config.from_object(config_cls)

    app.config['JWT_SECRET_KEY'] = app.config.get('SECRET_KEY', 'super-secret-jwt')

    bcrypt.init_app(app)
    jwt.init_app(app)

    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
