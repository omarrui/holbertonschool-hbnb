"""Tests for Amenity model and API using unittest."""

import unittest
from app.models.amenity import Amenity
from app import create_app


class TestAmenityModel(unittest.TestCase):
    """Unit tests for the Amenity model."""

    def test_amenity_creation_valid(self):
        amenity = Amenity(name="Wi-Fi")
        self.assertEqual(amenity.name, "Wi-Fi")

    def test_amenity_creation_empty_name(self):
        with self.assertRaises(ValueError):
            Amenity(name="")

    def test_amenity_creation_long_name(self):
        with self.assertRaises(ValueError):
            Amenity(name="A" * 51)

    def test_amenity_setter_valid(self):
        amenity = Amenity(name="Piscine")
        amenity.name = "Barbecue"
        self.assertEqual(amenity.name, "Barbecue")

    def test_amenity_setter_invalid(self):
        amenity = Amenity(name="Piscine")
        with self.assertRaises(ValueError):
            amenity.name = ""
        with self.assertRaises(ValueError):
            amenity.name = "B" * 51

    def test_amenity_to_dict(self):
        amenity = Amenity(name="Wi-Fi")
        d = amenity.to_dict()
        self.assertIn("id", d)
        self.assertIn("created_at", d)
        self.assertIn("updated_at", d)
        self.assertEqual(d["name"], "Wi-Fi")

    def test_amenity_multiple_setter(self):
        amenity = Amenity(name="Piscine")
        amenity.name = "Barbecue"
        amenity.name = "Sauna"
        self.assertEqual(amenity.name, "Sauna")

class TestAmenityAPI(unittest.TestCase):
    """Integration tests for Amenity API endpoints."""

    def setUp(self):
        """Set up Flask test client."""
        app = create_app()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_api_create_amenity_valid(self):
        r = self.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
        self.assertEqual(r.status_code, 201)
        self.assertIn("id", r.json)
        self.assertEqual(r.json["name"], "Wi-Fi")

    def test_api_create_amenity_empty_name(self):
        r = self.client.post('/api/v1/amenities/', json={"name": ""})
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.json)

    def test_api_create_amenity_long_name(self):
        r = self.client.post('/api/v1/amenities/', json={"name": "A" * 51})
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.json)

    def test_api_get_all_amenities(self):
        self.client.post('/api/v1/amenities/', json={"name": "Piscine"})
        r = self.client.get('/api/v1/amenities/')
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json, list)
        self.assertTrue(any(a["name"] == "Piscine" for a in r.json))

    def test_api_get_amenity_by_id(self):
        created = self.client.post('/api/v1/amenities/', json={"name": "Sauna"}).json
        amenity_id = created["id"]
        r = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json["id"], amenity_id)
        self.assertEqual(r.json["name"], "Sauna")

    def test_api_get_amenity_not_found(self):
        r = self.client.get('/api/v1/amenities/doesnotexist')
        self.assertEqual(r.status_code, 404)
        self.assertIn("error", r.json)

    def test_api_update_amenity_valid(self):
        created = self.client.post('/api/v1/amenities/', json={"name": "Jacuzzi"}).json
        amenity_id = created["id"]
        r = self.client.put(f'/api/v1/amenities/{amenity_id}', json={"name": "Hammam"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json["name"], "Hammam")

    def test_api_update_amenity_invalid_name(self):
        created = self.client.post('/api/v1/amenities/', json={"name": "Spa"}).json
        amenity_id = created["id"]
        r = self.client.put(f'/api/v1/amenities/{amenity_id}', json={"name": ""})
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.json)

    def test_api_update_amenity_not_found(self):
        r = self.client.put('/api/v1/amenities/doesnotexist', json={"name": "NewName"})
        self.assertEqual(r.status_code, 404)
        self.assertIn("error", r.json)


if __name__ == "__main__":
    unittest.main(verbosity=2)
