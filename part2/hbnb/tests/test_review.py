"""Tests for Review model and APIs."""

import unittest
from uuid import uuid4
from app import create_app


class TestReviewEndpoints(unittest.TestCase):
    """Test cases for Review API endpoints."""

    def setUp(self):
        """Set up test client and create test user and place."""
        self.app = create_app()
        self.client = self.app.test_client()

        unique_email = f"alice.{uuid4().hex}@example.com"
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": unique_email
        })
        self.assertEqual(
            user_response.status_code, 201,
            msg=f"User POST failed: {getattr(user_response, 'json', user_response.data)}"
        )

        self.user_id = user_response.json.get("id") or user_response.json.get("id_user")
        self.assertIsNotNone(self.user_id, "User id not found in response")

        place_response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(
            place_response.status_code, 201,
            msg=f"Place POST failed: {getattr(place_response, 'json', place_response.data)}"
        )
        self.place_id = place_response.json["id"]

    def test_create_review(self):
        """Test creating a review with valid data."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["text"], "Great place to stay!")
        self.assertEqual(response.json["rating"], 5)
        self.assertEqual(response.json["user_id"], self.user_id)
        self.assertEqual(response.json["place_id"], self.place_id)
        self.assertIn("id", response.json)

        self.review_id = response.json["id"]

    def test_create_review_empty_text(self):
        """Test that creating a review with empty text fails."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_create_review_invalid_rating(self):
        """Test that creating a review with invalid rating fails."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Nice place",
            "rating": 6,
            "user_id": self.user_id,
            "place_id": self.place_id
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_create_review_invalid_user_id(self):
        """Test that creating a review with invalid user_id fails."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Nice place",
            "rating": 4,
            "user_id": "invalid-user-id",
            "place_id": self.place_id
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_create_review_invalid_place_id(self):
        """Test that creating a review with invalid place_id fails."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Nice place",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": "invalid-place-id"
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_get_all_reviews(self):
        """Test getting all reviews."""
        self.client.post('/api/v1/reviews/', json={
            "text": "Great experience!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })

        response = self.client.get('/api/v1/reviews/')

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)

    def test_get_review_by_id(self):
        """Test getting a specific review by ID."""
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Amazing views!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })

        review_id = create_response.json["id"]

        response = self.client.get(f'/api/v1/reviews/{review_id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["id"], review_id)
        self.assertEqual(response.json["text"], "Amazing views!")
        self.assertEqual(response.json["rating"], 5)

    def test_get_reviews_by_place(self):
        """Test getting all reviews for a specific place."""
        self.client.post('/api/v1/reviews/', json={
            "text": "Great location!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })

        self.client.post('/api/v1/reviews/', json={
            "text": "Very clean",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })

        response = self.client.get(f'/api/v1/reviews/places/{self.place_id}/reviews')

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 2)

    def test_get_nonexistent_review(self):
        """Test getting a review that doesn't exist."""
        response = self.client.get('/api/v1/reviews/nonexistent-id')
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json)

    def test_update_review(self):
        """Test updating a review's attributes."""
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Good place",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })

        review_id = create_response.json["id"]

        update_response = self.client.put(
            f'/api/v1/reviews/{review_id}',
            json={"text": "Much better than initially thought", "rating": 4}
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertIn("message", update_response.json)

        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.json["text"], "Much better than initially thought")
        self.assertEqual(get_response.json["rating"], 4)

    def test_update_review_invalid_data(self):
        """Test updating a review with invalid data."""
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Good place",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })

        review_id = create_response.json["id"]

        update_response = self.client.put(
            f'/api/v1/reviews/{review_id}',
            json={"text": "", "rating": 6}
        )

        self.assertEqual(update_response.status_code, 400)
        self.assertIn("error", update_response.json)

    def test_delete_review(self):
        """Test deleting a review."""
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Review to delete",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })

        review_id = create_response.json["id"]

        delete_response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(delete_response.status_code, 200)
        self.assertIn("message", delete_response.json)

        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
