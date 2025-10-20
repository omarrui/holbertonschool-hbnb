"""Tests for User model and APIs."""

import unittest
from app import create_app
from app.models.user import User

class TestUserModel(unittest.TestCase):
    """Test cases for User model."""

    def test_user_creation(self):
        """Test successful User creation with valid data."""
        user = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
        self.assertEqual(user.first_name, "Alice")
        self.assertEqual(user.last_name, "Smith")
        self.assertEqual(user.email, "alice.smith@example.com")

    def test_user_creation_empty_first_name(self):
        """Test that User creation raises ValueError with empty first name."""
        with self.assertRaises(ValueError):
            User(first_name="", last_name="Smith", email="alice.smith@example.com")

    def test_user_creation_invalid_email(self):
        """Test that User creation raises ValueError with invalid email."""
        with self.assertRaises(ValueError):
            User(first_name="Alice", last_name="Smith", email="alice.smithexample.com")

    def test_user_setters(self):
        """Test setting user attributes."""
        user = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
        user.first_name = "Bob"
        user.last_name = "Brown"
        user.email = "bob.brown@example.com"
        self.assertEqual(user.first_name, "Bob")
        self.assertEqual(user.last_name, "Brown")
        self.assertEqual(user.email, "bob.brown@example.com")

    def test_user_setter_invalid_email(self):
        """Test setting invalid email raises ValueError."""
        user = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
        with self.assertRaises(ValueError):
            user.email = "invalidemail"

    def test_user_to_dict(self):
        """Test to_dict method returns correct keys."""
        user = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
        d = user.to_dict()
        self.assertEqual(d["first_name"], "Alice")
        self.assertEqual(d["last_name"], "Smith")
        self.assertEqual(d["email"], "alice.smith@example.com")
        self.assertIn("id_user", d)

class TestUserEndpoints(unittest.TestCase):
    """Test cases for User API endpoints."""

    def setUp(self):
        """Set up test client."""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        """Test creating a user with valid data."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice.smith@example.com"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["first_name"], "Alice")
        self.assertEqual(response.json["last_name"], "Smith")
        self.assertEqual(response.json["email"], "alice.smith@example.com")
        self.assertIn("id_user", response.json)

        self.user_id = response.json["id_user"]

    def test_create_user_empty_first_name(self):
        """Test that creating a user with empty first name fails."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Smith",
            "email": "alice.smith@example.com"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_create_user_invalid_email(self):
        """Test that creating a user with invalid email fails."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice.smithexample.com"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_get_all_users(self):
        """Test getting all users."""
        self.client.post('/api/v1/users/', json={
            "first_name": "Bob",
            "last_name": "Brown",
            "email": "bob.brown@example.com"
        })
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)

    def test_get_user_by_id(self):
        """Test getting a specific user by ID."""
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "Charlie",
            "last_name": "White",
            "email": "charlie.white@example.com"
        })
        user_id = create_response.json["id_user"]
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["id_user"], user_id)
        self.assertEqual(response.json["first_name"], "Charlie")

    def test_get_user_not_found(self):
        """Test getting a user that doesn't exist."""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json)

    def test_update_user(self):
        """Test updating a user's attributes."""
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "Daisy",
            "last_name": "Green",
            "email": "daisy.green@example.com"
        })
        user_id = create_response.json["id_user"]
        update_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "DaisyUpdated",
            "last_name": "Green",
            "email": "daisy.updated@example.com"
        })
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json["first_name"], "DaisyUpdated")
        self.assertEqual(update_response.json["email"], "daisy.updated@example.com")

    def test_update_user_invalid_email(self):
        """Test updating a user with invalid email fails."""
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "Eve",
            "last_name": "Black",
            "email": "eve.black@example.com"
        })
        user_id = create_response.json["id_user"]
        update_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Eve",
            "last_name": "Black",
            "email": "invalidemail"
        })
        self.assertEqual(update_response.status_code, 400)
        self.assertIn("error", update_response.json)

    def test_update_user_not_found(self):
        """Test updating a user that doesn't exist."""
        update_response = self.client.put('/api/v1/users/nonexistent-id', json={
            "first_name": "Ghost",
            "last_name": "User",
            "email": "ghost.user@example.com"
        })
        self.assertEqual(update_response.status_code, 404)
        self.assertIn("error", update_response.json)

if __name__ == '__main__':
    unittest.main()