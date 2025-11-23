from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

def serialize_amenity(a):
    return {"id": a.id, "name": a.name}

MAX_NAME_LEN = 50

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new amenity (admin only)"""
        identity = get_jwt_identity()
        if isinstance(identity, dict):
            current_user = identity.get('id') or identity.get('user_id')
            is_admin = bool(identity.get('is_admin', False))
        else:
            current_user = identity
            current_user_obj = facade.get_user(current_user)
            is_admin = getattr(current_user_obj, 'is_admin', False) if current_user_obj else False
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403

        data = api.payload or {}
        name = (data.get("name") or "").strip()

        if not name:
            return {"error": "name is required"}, 400
        if len(name) > MAX_NAME_LEN:
            return {"error": f"name must be <= {MAX_NAME_LEN} characters"}, 400

        try:
            amenity = facade.create_amenity({"name": name})
        except ValueError as e:
            return {"error": str(e)}, 400

        return serialize_amenity(amenity), 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [serialize_amenity(a) for a in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return serialize_amenity(amenity), 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity (admin only)"""
        identity = get_jwt_identity()
        if isinstance(identity, dict):
            current_user = identity.get('id') or identity.get('user_id')
            is_admin = bool(identity.get('is_admin', False))
        else:
            current_user = identity
            current_user_obj = facade.get_user(current_user)
            is_admin = getattr(current_user_obj, 'is_admin', False) if current_user_obj else False
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404

        data = api.payload or {}
        name = (data.get("name") or "").strip()

        if not name:
            return {"error": "name is required"}, 400
        if len(name) > MAX_NAME_LEN:
            return {"error": f"name must be <= {MAX_NAME_LEN} characters"}, 400

        try:
            updated = facade.update_amenity(amenity_id, {"name": name})
        except ValueError as e:
            return {"error": str(e)}, 400

        return serialize_amenity(updated), 200
