from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

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
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner not found')
    def post(self):
        """Register a new place"""
        try:
            place_data = api.payload
            # Check owner existence
            owner = facade.get_user(place_data.get("owner_id"))
            if not owner:
                return {"error": "Owner not found"}, 404
            # Check for duplicate title
            for p in facade.get_all_places():
                if p.title == place_data["title"]:
                    return {"error": "Title already used"}, 400
            # Validate amenities
            amenities_ids = place_data.get("amenities", [])
            for amenity_id in amenities_ids:
                if not facade.get_amenity(amenity_id):
                    return {"error": f"Amenity {amenity_id} not found"}, 400
            new_place = facade.create_place(place_data)
            # amenities is a list of IDs, return as such
            return {
                "id": new_place.id,
                "title": new_place.title,
                "description": new_place.description,
                "price": new_place.price,
                "latitude": new_place.latitude,
                "longitude": new_place.longitude,
                "owner_id": new_place.owner_id,
                "amenities": new_place.amenities
            }, 201
        except (ValueError, KeyError) as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [
            {
                "id": place.id,
                "title": place.title,
                "latitude": place.latitude,
                "longitude": place.longitude
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
            return {"error": "Place not found"}, 404
        owner = facade.get_user(place.owner_id)
        # amenities is a list of IDs, fetch their objects
        amenities_objs = []
        for amenity_id in getattr(place, "amenities", []):
            amenity = facade.get_amenity(amenity_id)
            if amenity:
                amenities_objs.append({"id": amenity.id, "name": amenity.name})
        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": {
                "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email
            } if owner else None,
            "amenities": amenities_objs
        }, 200

    @api.expect(place_model)  # validate=True is NOT used here
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information (partial update allowed)"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        data = api.payload

        allowed_fields = {"title", "description", "price", "latitude", "longitude", "owner_id", "amenities"}
        # If no data, return 400
        if not data:
            return {"error": "No valid fields to update"}, 400
        # If any unknown fields, return 400
        if any(field not in allowed_fields for field in data):
            return {"error": "No valid fields to update"}, 400

        # Validate fields if present
        if "title" in data:
            if not isinstance(data["title"], str) or len(data["title"].strip()) < 3:
                return {"error": "Le titre doit être une chaîne de 3 caractères minimum."}, 400
            # Check for duplicate title (excluding self)
            for p in facade.get_all_places():
                if p.title == data["title"] and p.id != place_id:
                    return {"error": "Title already used"}, 400
        if "latitude" in data:
            if not isinstance(data["latitude"], (int, float)) or not (-90 <= data["latitude"] <= 90):
                return {"error": "La latitude doit être comprise entre -90 et 90."}, 400
        if "longitude" in data:
            if not isinstance(data["longitude"], (int, float)) or not (-180 <= data["longitude"] <= 180):
                return {"error": "La longitude doit être comprise entre -180 et 180."}, 400
        if "price" in data:
            if data["price"] is None or data["price"] < 0:
                return {"error": "Le prix doit être un nombre positif."}, 400
        if "owner_id" in data:
            owner = facade.get_user(data["owner_id"])
            if not owner:
                return {"error": "Owner not found"}, 404
        if "amenities" in data:
            for amenity_id in data["amenities"]:
                if not facade.get_amenity(amenity_id):
                    return {"error": f"Amenity {amenity_id} not found"}, 400

        try:
            place.update(data)
            return {"message": "Place updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        facade.place_repo.delete(place_id)
        return {"message": "Place deleted successfully"}, 200

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {"error": "Place not found"}, 404
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id
            }
            for review in reviews
        ], 200
