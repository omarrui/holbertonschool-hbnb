from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place'),
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating between 1 and 5')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new review"""
        data = api.payload or {}
        try:
            new_review = facade.create_review(data)
        except ValueError as e:
            msg = str(e)
            if 'not found' in msg.lower():
                return {'error': msg}, 404
            return {'error': msg}, 400

        return new_review.to_dict(), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        rev = facade.get_review(review_id)
        if not rev:
            return {'error': 'Review not found'}, 404
        return rev.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        data = api.payload or {}
        try:
            updated = facade.update_review(review_id, data)
        except ValueError as e:
            msg = str(e)
            if 'not found' in msg.lower():
                return {'error': msg}, 404
            return {'error': msg}, 400

        if not updated:
            return {'error': 'Review not found'}, 404
        return updated.to_dict(), 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review by ID"""
        ok = facade.delete_review(review_id)
        if not ok:
            return {'error': 'Review not found'}, 404
<<<<<<< HEAD
        return {'message': 'Review deleted successfully'}, 200
=======
        return {}, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        res = facade.get_reviews_by_place(place_id)
        if res is None:
            return {'error': 'Place not found'}, 404
        return [r.to_dict() for r in res], 200
>>>>>>> Dev-holby_w
