from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace("places", description="Place operations")

place_model = api.model("Place", {
    "title": fields.String(required=True, description="Title of the place"),
    "description": fields.String(description="Description of the place"),
    "price": fields.Float(required=True, description="Price per night"),
    # Latitude/longitude rendus optionnels pour permettre création sans géolocalisation immédiate
    "latitude": fields.Float(required=False, description="Latitude of the place (optional)"),
    "longitude": fields.Float(required=False, description="Longitude of the place (optional)"),
    # owner_id devient optionnel: sera forcé au current user si non admin
    "owner_id": fields.String(required=False, description="ID of the owner (auto-set if omitted)"),
    "amenities": fields.List(fields.String, description="List of amenities IDs")
})

place_update_model = api.model("PlaceUpdate", {
    "title": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "latitude": fields.Float,
    "longitude": fields.Float,
    "amenities": fields.List(fields.String),
    "owner_id": fields.String,
})

def _serialize_place(p):
    return p.to_dict() if hasattr(p, "to_dict") else {
        "id": getattr(p, "id", None),
        "title": getattr(p, "title", None),
        "description": getattr(p, "description", None),
        "price": getattr(p, "price", None),
        "latitude": getattr(p, "latitude", None),
        "longitude": getattr(p, "longitude", None),
        "owner_id": getattr(p, "owner", None),
    }

@api.route("/")
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    @api.response(404, "Owner or amenity not found")
    @jwt_required()
    def post(self):
        """Create a new place (authenticated users only). Owner is set to the current user."""
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
        # Assigner automatiquement owner_id si absent (admin ou non)
        if not data.get('owner_id'):
            data['owner_id'] = current_user
        try:
            place = facade.create_place(data)
        except ValueError as e:
            msg = str(e)
            if "not found" in msg.lower():
                return {"error": msg}, 404
            return {"error": msg}, 400
        return _serialize_place(place), 201

    @api.response(200, "List of all places")
    def get(self):
        """Get all places"""
        places = facade.get_all_places()
        serialized = []
        for p in places:
            data = _serialize_place(p)
            ratings = [getattr(r, 'rating', None) for r in getattr(p, 'reviews', []) if getattr(r, 'rating', None) is not None]
            count = len(ratings)
            avg = round(sum(ratings) / count, 2) if count else None
            data['average_rating'] = avg
            data['review_count'] = count
            serialized.append(data)
        return serialized, 200

@api.route("/<place_id>")
class PlaceResource(Resource):
    @api.response(200, "Place details retrieved")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get a specific place by ID"""
        res = facade.get_place(place_id)
        if not res:
            return {"error": "Place not found"}, 404
        place = res["place"]
        data = _serialize_place(place)
        data["amenities"] = [{"id": a.id, "name": getattr(a, "name", None)} for a in res.get("amenities", [])]
        # Correct review serialization: use comment + rating; include user_id for potential UI
        data["reviews"] = [{
            "id": r.id,
            "comment": getattr(r, "comment", None),
            "rating": getattr(r, "rating", None),
            "user_id": getattr(r, "user_id", None)
        } for r in res.get("reviews", [])]
        # Host (owner) details for display: add human name instead of raw id
        owner = res.get("owner")
        if owner:
            data["host"] = {
                "id": owner.id,
                "first_name": getattr(owner, "first_name", None),
                "last_name": getattr(owner, "last_name", None),
                "full_name": f"{getattr(owner, 'first_name', '')} {getattr(owner, 'last_name', '')}".strip()
            }
        else:
            data["host"] = None
        # Average rating and count
        ratings = [getattr(r, 'rating', None) for r in res.get('reviews', []) if getattr(r, 'rating', None) is not None]
        count = len(ratings)
        avg = round(sum(ratings) / count, 2) if count else None
        data['average_rating'] = avg
        data['review_count'] = count
        return data, 200

    @api.expect(place_update_model, validate=True)
    @api.response(200, "Place updated successfully")
    @api.response(404, "Place or owner not found")
    @api.response(400, "Invalid input data")
    @jwt_required()
    def put(self, place_id):
        """Update an existing place (only owner can update)."""
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

        res = facade.get_place(place_id)
        if not res:
            return {"error": "Place not found"}, 404
        place = res["place"]

        if not is_admin and getattr(place, "owner", None) != current_user:
            return {"error": "Unauthorized action"}, 403

        data = api.payload or {}

        if not is_admin and "owner_id" in data:
            return {"error": "You cannot change owner_id"}, 400
        try:
            updated = facade.update_place(place_id, data)
        except ValueError as e:
            msg = str(e)
            if "not found" in msg.lower():
                return {"error": msg}, 404
            return {"error": msg}, 400
        if not updated:
            return {"error": "Place not found"}, 404
        return _serialize_place(updated), 200

    @api.response(200, "Place deleted successfully")
    @api.response(404, "Place not found")
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def delete(self, place_id):
        """Delete a place (admin only)."""
        identity = get_jwt_identity()
        jwt_claims = None
        try:
            from flask_jwt_extended import get_jwt
            jwt_claims = get_jwt()
        except Exception:
            jwt_claims = None
        is_admin = False
        if isinstance(identity, dict):
            is_admin = bool(identity.get('is_admin', False))
        else:
            if jwt_claims and 'is_admin' in jwt_claims:
                is_admin = bool(jwt_claims.get('is_admin', False))
            else:
                current_user_obj = facade.get_user(identity)
                is_admin = getattr(current_user_obj, 'is_admin', False) if current_user_obj else False
        if not is_admin:
            return {"error": "Admin privileges required"}, 403
        ok = facade.delete_place(place_id)
        if not ok:
            return {"error": "Place not found"}, 404
        return {"message": "Place deleted successfully"}, 200
