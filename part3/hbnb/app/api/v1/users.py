from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import get_jwt
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new user (admin only)"""
        # Determine admin status from JWT claims
        jwt_claims = None
        try:
            jwt_claims = get_jwt()
        except Exception:
            jwt_claims = None

        is_admin = False
        if jwt_claims and 'is_admin' in jwt_claims:
            is_admin = bool(jwt_claims.get('is_admin', False))
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload or {}

        existing_user = facade.get_user_by_email(user_data.get('email'))
        if existing_user:
            return {'error': 'Email already registered'}, 400
        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        return [u.to_dict() for u in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, user_id):
        """Update a user's information.

        Admins can update any user (including email/password).
        Non-admins can only update their own profile and cannot change email/password.
        """
        identity = get_jwt_identity()
        jwt_claims = None
        try:
            jwt_claims = get_jwt()
        except Exception:
            jwt_claims = None

        is_admin = False
        if isinstance(identity, dict):
            current_user = identity.get('id') or identity.get('user_id')
            is_admin = bool(identity.get('is_admin', False))
        else:
            current_user = identity
            if jwt_claims and 'is_admin' in jwt_claims:
                is_admin = bool(jwt_claims.get('is_admin', False))
            else:
                current_user_obj = facade.get_user(current_user)
                is_admin = bool(current_user_obj and getattr(current_user_obj, 'is_admin', False))

        # Non-admins can only edit themselves
        if not is_admin and user_id != current_user:
            # non-admin attempting to modify another user's data
            return {'error': 'Unauthorized action'}, 403

        user_data = api.payload or {}

        # If non-admin, disallow changing email or password through this endpoint
        if not is_admin and ('email' in user_data or 'password' in user_data):
            return {'error': 'You cannot modify email or password'}, 400

        # If admin and email provided, ensure uniqueness
        if is_admin and user_data.get('email'):
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        try:
            updated_user = facade.update_user(user_id, user_data)
            return updated_user.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
