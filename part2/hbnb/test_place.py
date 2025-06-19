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
