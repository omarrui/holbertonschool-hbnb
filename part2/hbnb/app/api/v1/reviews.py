from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_in_model = api.model('ReviewIn', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place'),
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
})

def serialize_review(r):
    return {
        'id': r.id,
        'text': r.text,
        'rating': r.rating,
        'user_id': r.user_id,
        'place_id': r.place_id,
    }

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_in_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review."""
        data = api.payload or {}
        try:
            new_review = facade.create_review(data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return serialize_review(new_review), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews."""
        reviews = facade.get_all_reviews()
        return [serialize_review(r) for r in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID."""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return serialize_review(review), 200

    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information."""
        data = api.payload or {}

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        try:
            updated = facade.update_review(review_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400

        if not updated:
            return {'error': 'Review not found'}, 404

        return {'message': 'Review updated successfully'}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review."""
        ok = facade.delete_review(review_id)
        if not ok:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place."""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {'error': 'Place not found'}, 404
        return [serialize_review(r) for r in reviews], 200
