from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from app.services import facade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

register_model = api.model('Register', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password (min 6 chars)')
})

@api.route('/login')
class LoginResource(Resource):
    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Invalid credentials')
    def post(self):
        data = request.get_json(silent=True) or {}
        email = (data.get('email') or '').strip().lower()
        password = data.get('password')

        if not email or not password:
            return {'error': 'email and password are required'}, 400

        user = facade.get_user_by_email(email)
        if not user or not user.check_password(password):
            return {'error': 'Invalid email or password'}, 401

        claims = {
            'user_id': user.id,
            'email': user.email,
            'is_admin': getattr(user, 'is_admin', False)
        }

        access_token = create_access_token(identity=user.id, additional_claims=claims)

        return {
            'access_token': access_token,
            'token_type': 'Bearer'
        }, 200

@api.route('/register')
class RegisterResource(Resource):
    @api.expect(register_model, validate=True)
    @api.response(201, 'User registered')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Email already exists')
    def post(self):
        data = request.get_json(silent=True) or {}
        first_name = (data.get('first_name') or '').strip()
        last_name = (data.get('last_name') or '').strip()
        email = (data.get('email') or '').strip().lower()
        password = data.get('password') or ''

        if not all([first_name, last_name, email, password]):
            return {'error': 'All fields are required'}, 400
        if '@' not in email or '.' not in email:
            return {'error': 'Invalid email format'}, 400
        if len(password) < 6:
            return {'error': 'Password too short (min 6)'}, 400

        # Check duplicate first
        existing = facade.get_user_by_email(email)
        if existing:
            return {'error': 'Email already exists'}, 409

        try:
            user = facade.create_user({
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password
            })
        except IntegrityError:
            return {'error': 'Email already exists'}, 409
        except Exception as e:
            return {'error': f'Unable to register: {e}'}, 400

        claims = {
            'user_id': user.id,
            'email': user.email,
            'is_admin': getattr(user, 'is_admin', False)
        }
        access_token = create_access_token(identity=user.id, additional_claims=claims)
        return {'access_token': access_token, 'token_type': 'Bearer'}, 201
