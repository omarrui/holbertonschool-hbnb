from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt

api = Namespace('reviews', description='Review operations')

review_in_model = api.model('ReviewIn', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
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
    @jwt_required(optional=True)
    @api.expect(review_in_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review (authenticated only). Prevent self-review and duplicates."""
        identity = get_jwt_identity()
        jwt_claims = None
        try:
            from flask_jwt_extended import get_jwt
            jwt_claims = get_jwt()
        except Exception:
            jwt_claims = None

        is_admin = False
        if isinstance(identity, dict):
            current_user = identity.get('id') or identity.get('user_id')
            is_admin = bool(identity.get('is_admin', False))
        else:
            current_user = identity
            if jwt_claims and 'is_admin' in jwt_claims:
                is_admin = bool(jwt_claims.get('is_admin', False))
            else:
                current_user_obj = facade.get_user(current_user)
                is_admin = getattr(current_user_obj, 'is_admin', False) if current_user_obj else False
        data = api.payload or {}

        place_id = data.get('place_id')
        if not place_id:
            return {'error': 'place_id is required'}, 400

        place_res = facade.get_place(place_id)
        if not place_res:
            return {'error': 'Place not found'}, 404

        place = place_res.get('place')
        # Prevent users from reviewing their own place (admins can bypass)
        if not is_admin and getattr(place, 'owner', None) == current_user:
            return {'error': 'You cannot review your own place'}, 400

        # Prevent duplicate reviews by same user on same place (admins can bypass)
        if not is_admin:
            reviews = facade.get_reviews_by_place(place_id) or []
            for r in reviews:
                if getattr(r, 'user_id', None) == current_user:
                    return {'error': 'You have already reviewed this place'}, 400

        data['user_id'] = current_user
        try:
            new_review = facade.create_review(data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return serialize_review(new_review), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        reviews = facade.get_all_reviews()
        return [serialize_review(r) for r in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return serialize_review(review), 200

    @jwt_required(optional=True)
    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information (only author can update)."""
        identity = get_jwt_identity()
        jwt_claims = None
        try:
            from flask_jwt_extended import get_jwt
            jwt_claims = get_jwt()
        except Exception:
            jwt_claims = None

        is_admin = False
        if isinstance(identity, dict):
            current_user = identity.get('id') or identity.get('user_id')
            is_admin = bool(identity.get('is_admin', False))
        else:
            current_user = identity
            if jwt_claims and 'is_admin' in jwt_claims:
                is_admin = bool(jwt_claims.get('is_admin', False))
            else:
                current_user_obj = facade.get_user(current_user)
                is_admin = getattr(current_user_obj, 'is_admin', False) if current_user_obj else False
        data = api.payload or {}

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if getattr(review, 'user_id', None) != current_user and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        try:
            updated = facade.update_review(review_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400

        if not updated:
            return {'error': 'Review not found'}, 404

        return {'message': 'Review updated successfully'}, 200

    @jwt_required(optional=True)
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review (only author can delete)."""
        identity = get_jwt_identity()
        jwt_claims = None
        try:
            from flask_jwt_extended import get_jwt
            jwt_claims = get_jwt()
        except Exception:
            jwt_claims = None

        is_admin = False
        if isinstance(identity, dict):
            current_user = identity.get('id') or identity.get('user_id')
            is_admin = bool(identity.get('is_admin', False))
        else:
            current_user = identity
            if jwt_claims and 'is_admin' in jwt_claims:
                is_admin = bool(jwt_claims.get('is_admin', False))
            else:
                current_user_obj = facade.get_user(current_user)
                is_admin = getattr(current_user_obj, 'is_admin', False) if current_user_obj else False
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if getattr(review, 'user_id', None) != current_user and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        ok = facade.delete_review(review_id)
        if not ok:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {'error': 'Place not found'}, 404
        return [serialize_review(r) for r in reviews], 200
