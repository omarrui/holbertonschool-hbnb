from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.place import Place

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=True, description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
    'owner_id': fields.String(required=True, description='ID of the place owner'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place"""
        place_data = api.payload
        
        # Validate owner exists
        owner = facade.get_user(place_data['owner_id'])
        if not owner:
            return {'error': 'Owner not found'}, 404
            
        try:
            new_place = facade.create_place(place_data)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id,
                'amenities': new_place.amenities
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve all places"""
        places = facade.get_all_places()
        return [
            {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': place.owner_id
            }
            for place in places
        ], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
            
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner_id,
            'amenities': place.amenities
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update place details"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
            
        data = api.payload
        try:
            facade.update_place(place_id, data)
            return {'message': 'Place updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
            
        facade.place_repo.delete(place_id)
        return {'message': 'Place deleted successfully'}, 200

@api.route('/<place_id>/reviews')
class PlaceReviews(Resource):
    @api.response(200, 'Reviews retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
            
        reviews = facade.get_reviews_by_place(place_id)
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            }
            for review in reviews
        ], 200