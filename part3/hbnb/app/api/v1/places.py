from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("places", description="Place operations")

place_model = api.model("Place", {
    "title": fields.String(required=True, description="Title of the place"),
    "description": fields.String(description="Description of the place"),
    "price": fields.Float(required=True, description="Price per night"),
    "latitude": fields.Float(required=True, description="Latitude of the place"),
    "longitude": fields.Float(required=True, description="Longitude of the place"),
    "owner_id": fields.String(required=True, description="ID of the owner"),
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
    def post(self):
        """Create a new place"""
        data = api.payload or {}
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
        return [_serialize_place(p) for p in places], 200

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
        data["reviews"] = [{"id": r.id, "text": getattr(r, "text", None)} for r in res.get("reviews", [])]
        return data, 200

    @api.expect(place_update_model, validate=True)
    @api.response(200, "Place updated successfully")
    @api.response(404, "Place or owner not found")
    @api.response(400, "Invalid input data")
    def put(self, place_id):
        """Update an existing place"""
        data = api.payload or {}
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
