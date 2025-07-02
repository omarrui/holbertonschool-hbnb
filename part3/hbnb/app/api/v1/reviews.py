from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, min=1, max=5, description='Rating from 1 to 5'),
    'user_id': fields.String(required=False, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place not found')
    def post(self):
        """Create a new review"""
        current_user = get_jwt_identity()
        review_data = api.payload

        # Set user_id to current user (admins can also set different user_id)
        is_admin = current_user.get('is_admin', False)
        if not is_admin or 'user_id' not in review_data:
            review_data['user_id'] = current_user['id']

        # Retrieve the place
        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404

        # Check if the user owns the place (unless admin)
        if not is_admin and place.owner_id == current_user['id']:
            return {'error': 'You cannot review your own place'}, 400

        # Check if the user has already reviewed the place (unless admin)
        if not is_admin:
            existing_review = facade.get_review_by_user_and_place(current_user['id'], review_data['place_id'])
            if existing_review:
                return {'error': 'You have already reviewed this place'}, 400

        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'place_id': new_review.place_id,
                'user_id': new_review.user_id
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
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

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
            
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    def put(self, review_id):
        """Update a review"""
        current_user = get_jwt_identity()
        review_data = api.payload

        # Retrieve the review
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        # Check authorization - admin can modify any review
        if not is_admin and review.user_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            facade.update_review(review_id, review_data)
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()

        # Retrieve the review
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        # Check authorization - admin can delete any review
        if not is_admin and review.user_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        # Delete the review
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200