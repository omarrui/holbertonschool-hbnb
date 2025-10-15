from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        data = api.payload or {}
        try:
            new_place = facade.create_place(data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return new_place.to_dict(), 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        # Return minimal fields as required
        result = []
        for p in places:
            result.append({'id': p.id, 'title': getattr(p, 'title', None), 'latitude': p.latitude, 'longitude': p.longitude})
        return result, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        res = facade.get_place(place_id)
        if not res:
            return {'error': 'Place not found'}, 404

        place = res['place']
        owner = res.get('owner')
        amenities = res.get('amenities', [])

        owner_data = None
        if owner:
            owner_data = {'id': owner.id, 'first_name': getattr(owner, 'first_name', None), 'last_name': getattr(owner, 'last_name', None), 'email': getattr(owner, 'email', None)}

        amenities_data = [{'id': a.id, 'name': getattr(a, 'name', None)} for a in amenities]

        reviews = res.get('reviews', [])
        reviews_data = [{'id': r.id, 'user_id': getattr(r, 'user_id', None), 'text': getattr(r, 'text', None)} for r in reviews]

        out = place.to_dict()
        out['owner'] = owner_data
        out['amenities'] = amenities_data
        out['reviews'] = reviews_data
        return out, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        data = api.payload or {}
        try:
            updated = facade.update_place(place_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400

        if not updated:
            return {'error': 'Place not found'}, 404

        return {'message': 'Place updated successfully'}, 200