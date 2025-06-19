import unittest
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        print('\n' + '-'*50)  # Add separator between tests

    def test_create_user_place(self):
        print("\nTest: Create User and Place")

        print("\n1. Creating user...")
        user_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "aaa@aaa.aa"
        }
        print(f"Request data: {user_data}")
        response1 = self.client.post('/api/v1/users/', json=user_data)
        self.assertEqual(response1.status_code, 201)
        print(f"Response (status {response1.status_code}): {response1.json}")
        
        user_id = response1.json['id']

        print("\n2. Creating place...")
        place_data = {
            "title": "My Place",
            "description": "A beautiful place",
            "price": 100.0,
            "latitude": 1.0,
            "longitude": 1.0,
            "owner_id": user_id,
            "amenities": []
        }
        print(f"Request data: {place_data}")
        response = self.client.post('/api/v1/places/', json=place_data)
        self.assertEqual(response.status_code, 201)
        print(f"Response (status {response.status_code}): {response.json}")

        place_id = response.json['id']

        print("\n3. Getting place...")
        get_response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(get_response.status_code, 200)
        print(f"Response (status {get_response.status_code}): {get_response.json}")

        print("\n4. Updating place...")
        update_response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "Updated My Place",
            "description": "updated A beautiful place",
            "price": 50.0,
            "latitude": 2.0,
            "longitude": 0.0,
            "owner_id": user_id,
            "amenities": []
        })
        self.assertEqual(update_response.status_code, 200)
        print(f"Response (status {update_response.status_code}): {update_response.json}")

    def test_get_all_places(self):
        print("\nTest: Getting all places")
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        print(f"Response (status {response.status_code}): {response.json}")
    
    def test_get_place_not_found(self):
        print("\nTest: Getting non-existent place")
        response = self.client.get('/api/v1/places/qsdqsqqds')
        self.assertEqual(response.status_code, 404)
        print(f"Response (status {response.status_code}): {response.json}")
        
    def test_place_with_amenities(self):
        print("\nTest: Creating place with amenities")

        # First create user and amenities
        user_data = {
            "first_name": "Test",
            "last_name": "Amenity",
            "email": "test@amenity.com"
        }
        user_res = self.client.post('/api/v1/users/', json=user_data)
        user_id = user_res.json['id']

        amenity1 = self.client.post('/api/v1/amenities/', json={"name": "WiFi"}).json['id']
        amenity2 = self.client.post('/api/v1/amenities/', json={"name": "Pool"}).json['id']

        place_data = {
            "title": "With Amenities",
            "description": "Nice place",
            "price": 120.0,
            "latitude": 0.0,
            "longitude": 0.0,
            "owner_id": user_id,
            "amenities": [amenity1, amenity2]
        }

        response = self.client.post('/api/v1/places/', json=place_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(amenity1, response.json["amenities"])
        self.assertIn(amenity2, response.json["amenities"])

    def test_delete_place(self):
        print("\nTest: Deleting a place")

        # Create user
        user_data = {
            "first_name": "John",
            "last_name": "Smith",
            "email": "john@example.com"
        }
        response = self.client.post('/api/v1/users/', json=user_data)
        user_id = response.json['id']

        # Create place
        place_data = {
            "title": "To Delete",
            "description": "This will be deleted",
            "price": 80.0,
            "latitude": 10.0,
            "longitude": 20.0,
            "owner_id": user_id,
            "amenities": []
        }
        response = self.client.post('/api/v1/places/', json=place_data)
        place_id = response.json['id']

        # Delete it
        delete_response = self.client.delete(f'/api/v1/places/{place_id}')
        self.assertEqual(delete_response.status_code, 200)
        print(f"Delete response: {delete_response.json}")

        # Check it's gone
        get_response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(get_response.status_code, 404)
    def test_create_place_missing_fields(self):
        print("\nTest: Creating place with missing fields")

        # Missing title
        bad_data = {
            "description": "Missing title",
            "price": 20.0,
            "latitude": 1.0,
            "longitude": 1.0,
            "owner_id": "some_id"
        }
        response = self.client.post('/api/v1/places/', json=bad_data)
        self.assertEqual(response.status_code, 400)
        print(f"Response (status {response.status_code}): {response.json}")

    def test_create_place_invalid_owner(self):
        print("\nTest: Creating place with invalid owner ID")

        place_data = {
            "title": "Invalid Owner",
            "description": "Invalid user",
            "price": 45.0,
            "latitude": 2.2,
            "longitude": 3.3,
            "owner_id": "nonexistent_id",
            "amenities": []
        }

        response = self.client.post('/api/v1/places/', json=place_data)
        self.assertEqual(response.status_code, 400)
