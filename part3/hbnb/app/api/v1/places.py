from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from app.models.place import Place

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=False, description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=False, description='Latitude of the place'),
    'longitude': fields.Float(required=False, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the place owner'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place"""
        current_user = get_jwt_identity()  # Get the authenticated user's identity
        place_data = api.payload

        # Add the owner_id to the place data
        place_data['owner_id'] = current_user['id']

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

    @jwt_required()
    def put(self, place_id):
        """Update a place's details"""
        current_user = get_jwt_identity()  # Get the authenticated user's identity
        place_data = api.payload

        # Retrieve the place
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Check if the current user is the owner of the place
        if place.owner_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        # Update the place
        updated_place = facade.update_place(place_id, place_data)
        return {
            'id': updated_place.id,
            'title': updated_place.title,
            'description': updated_place.description,
            'price': updated_place.price,
            'latitude': updated_place.latitude,
            'longitude': updated_place.longitude,
            'owner_id': updated_place.owner_id
        }, 200

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