from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
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
