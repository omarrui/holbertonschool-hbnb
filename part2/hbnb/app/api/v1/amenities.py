from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

def serialize_amenity(a):
    return {"id": a.id, "name": a.name}

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        data = api.payload or {}
        name = data.get("name", "").strip()
        if not name:
            return {"error": "Invalid input data"}, 400

        amenity = facade.create_amenity({"name": name})
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
    def put(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404

        data = api.payload or {}
        name = data.get("name", "").strip()
        if not name:
            return {"error": "Invalid input data"}, 400

        updated = facade.update_amenity(amenity_id, {"name": name})
        return serialize_amenity(updated), 200
