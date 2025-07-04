from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.user import User

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Validate email format
        if not User.is_valid_email(user_data['email']):
            return {'error': 'Invalid email'}, 400

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        users = facade.user_repo.get_all()
        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            for user in users
        ], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model)  # REMOVE validate=True
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user details (partial update allowed)"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        data = api.payload

        allowed_fields = {"first_name", "last_name", "email"}
        # If any unknown fields, return 400
        if not any(field in data for field in allowed_fields) or any(field not in allowed_fields for field in data):
            return {'error': 'No valid fields to update'}, 400

        # Validate only provided fields
        if "email" in data:
            if not User.is_valid_email(data['email']):
                return {'error': 'Invalid email'}, 400
            existing = facade.get_user_by_email(data['email'])
            if existing and existing.id != user_id:
                return {'error': 'Email already registered'}, 400
        if "first_name" in data and (not data["first_name"] or len(data["first_name"]) > 50):
            return {'error': 'First name is required and must be <= 50 characters'}, 400
        if "last_name" in data and (not data["last_name"] or len(data["last_name"]) > 50):
            return {'error': 'Last name is required and must be <= 50 characters'}, 400
        try:
            user.update(data)
            return {"message": "User updated successfully"}, 200
        except Exception as e:
            return {'error': str(e)}, 400
