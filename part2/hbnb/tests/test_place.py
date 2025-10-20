"""Tests for Place APIs."""

import unittest
import uuid
from app import create_app


class TestPlaceEndpoints(unittest.TestCase):
    """Tests des endpoints Place."""

    def setUp(self):
        """Client + création d'un user de test (email unique)."""
        self.app = create_app()
        self.client = self.app.test_client()

        unique_email = f"alice_{uuid.uuid4().hex[:8]}@example.com"

        resp = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": unique_email
        })

        self.assertEqual(
            resp.status_code, 201,
            msg=f"User POST failed: {getattr(resp, 'json', resp.data)}"
        )
        self.assertIn("id_user", resp.json)
        self.user_id = resp.json["id_user"]

    def create_place(self, overrides=None):
        """POST /places avec un payload par défaut, overridable."""
        payload = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id,
            "amenities": []
        }
        if overrides:
            payload.update(overrides)
        return self.client.post('/api/v1/places/', json=payload)

    def test_create_place(self):
        r = self.create_place()
        self.assertEqual(r.status_code, 201)
        self.assertIn("id", r.json)
        self.assertEqual(r.json["owner_id"], self.user_id)

    def test_create_place_empty_title(self):
        r = self.create_place({"title": ""})
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.json)

    def test_create_place_title_too_long(self):
        r = self.create_place({"title": "A" * 101})
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.json)

    def test_create_place_invalid_price(self):
        r = self.create_place({"price": -50})
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.json)

    def test_create_place_invalid_latitude(self):
        r = self.create_place({"latitude": 100})
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.json)

    def test_create_place_invalid_longitude(self):
        r = self.create_place({"longitude": 200})
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.json)

    def test_create_place_invalid_owner(self):
        r = self.create_place({"owner_id": "invalid-owner-id"})
        self.assertEqual(r.status_code, 404)
        self.assertIn("error", r.json)

    def test_get_all_places(self):
        self.create_place()
        r = self.client.get('/api/v1/places/')
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json, list)
        self.assertGreater(len(r.json), 0)

    def test_get_place_by_id(self):
        c = self.create_place()
        place_id = c.json["id"]
        r = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json["id"], place_id)

    def test_get_nonexistent_place(self):
        r = self.client.get('/api/v1/places/nonexistent-id')
        self.assertEqual(r.status_code, 404)
        self.assertIn("error", r.json)

    def test_update_place(self):
        c = self.create_place()
        place_id = c.json["id"]
        r = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "Luxury Apartment",
            "price": 200
        })
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json["title"], "Luxury Apartment")

    def test_update_place_empty_title(self):
        c = self.create_place()
        place_id = c.json["id"]
        r = self.client.put(f'/api/v1/places/{place_id}', json={"title": ""})
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.json)

    def test_update_place_title_too_long(self):
        c = self.create_place()
        place_id = c.json["id"]
        r = self.client.put(f'/api/v1/places/{place_id}', json={"title": "A" * 101})
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.json)

    def test_update_place_invalid_price(self):
        c = self.create_place()
        place_id = c.json["id"]
        r = self.client.put(f'/api/v1/places/{place_id}', json={"price": -10})
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.json)

    def test_update_place_invalid_latitude(self):
        c = self.create_place()
        place_id = c.json["id"]
        r = self.client.put(f'/api/v1/places/{place_id}', json={"latitude": 120})
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.json)

    def test_update_place_invalid_longitude(self):
        c = self.create_place()
        place_id = c.json["id"]
        r = self.client.put(f'/api/v1/places/{place_id}', json={"longitude": 200})
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.json)

    def test_update_place_invalid_owner(self):
        c = self.create_place()
        place_id = c.json["id"]
        r = self.client.put(f'/api/v1/places/{place_id}', json={"owner_id": "wrong-id"})
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.json)


if __name__ == '__main__':
    unittest.main()
