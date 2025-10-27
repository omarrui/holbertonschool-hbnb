# HolbertonBnB – RESTful API (Part 2)

A fully functional, well-structured RESTful API built with **Python** and **Flask-RESTX**, designed as the backend core of an Airbnb-like application.  
This project implements CRUD operations for **Users**, **Places**, **Amenities**, and **Reviews**, using clean architecture principles and complete test coverage.

---

## Overview

This API provides an in-memory implementation of a booking system.  
It focuses on **clarity, modularity, and correctness**, using a **Facade pattern** to separate business logic from persistence and routing layers.

All endpoints follow RESTful standards and include validation, structured error handling, and proper response formatting.

---

## Features

- CRUD endpoints for:
  - **Users**
  - **Places**
  - **Amenities**
  - **Reviews**
- Full data validation with Python property setters
- In-memory persistence layer (no database required)
- Facade layer for business logic
- Clean error management (HTTP 400, 404)
- 100% unit test coverage with `unittest`
- PEP8-compliant and no stray `print()` or logs

---

## Tech Stack

| Category | Technology |
|-----------|-------------|
| Language | Python 3 |
| Framework | Flask, Flask-RESTX |
| Testing | unittest |
| Architecture | Facade pattern + Repository pattern |
| Data Layer | InMemoryRepository |

---

## Project Structure


---

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```
---
## Installation and Setup
### 1. Clone the repository
bash
git clone https://github.com/<your-username>/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part2
### 2. Create a virtual environment and activate it
bash
python3 -m venv venv
source venv/bin/activate
### 3. Install dependencies
bash
pip install -r requirements.txt
### 4. Run the application
bash
python3 api/app.py The API will run locally at: http://127.0.0.1:5000/
Swagger UI will be available at : http://127.0.0.1:5000/api/v1/

---
## Core Entities
| Entity      | Description                                                                                                                |
| ----------- | -------------------------------------------------------------------------------------------------------------------------- |
| *User*    | Represents a platform user (with first name, last name, email, etc.). Passwords are never returned in responses.           |
| *Place*   | Represents a property listed by a user. Includes attributes like name, price, latitude, longitude, and linked amenities.   |
| *Amenity* | Represents a feature or service offered by a place (e.g., Wi-Fi, Pool).                                                    |
| *Review*  | Represents user feedback associated with a specific place. Includes review text, rating, and references to User and Place. |
---
## API Endpoints Overview
### Users
| Method | Endpoint                  | Description         |
| ------ | ------------------------- | ------------------- |
| POST | /api/v1/users/          | Create a new user   |
| GET  | /api/v1/users/          | Retrieve all users  |
| GET  | /api/v1/users/<user_id> | Retrieve user by ID |
| PUT  | /api/v1/users/<user_id> | Update user info    |
---
### Amenities
| Method | Endpoint                         | Description                 |
| ------ | -------------------------------- | --------------------------- |
| POST | /api/v1/amenities/             | Create a new amenity        |
| GET  | /api/v1/amenities/             | Retrieve all amenities      |
| GET  | /api/v1/amenities/<amenity_id> | Retrieve a specific amenity |
| PUT  | /api/v1/amenities/<amenity_id> | Update an amenity           |
---
### Places
| Method | Endpoint                    | Description                                                 |
| ------ | --------------------------- | ----------------------------------------------------------- |
| POST | /api/v1/places/           | Create a new place                                          |
| GET  | /api/v1/places/           | Retrieve all places                                         |
| GET  | /api/v1/places/<place_id> | Retrieve a specific place (includes owner info & amenities) |
| PUT  | /api/v1/places/<place_id> | Update a place                                              |
---
### Reviews
| Method   | Endpoint                      | Description                |
| -------- | ----------------------------- | -------------------------- |
| POST   | /api/v1/reviews/            | Create a new review        |
| GET    | /api/v1/reviews/            | Retrieve all reviews       |
| GET    | /api/v1/reviews/<review_id> | Retrieve a specific review |
| PUT    | /api/v1/reviews/<review_id> | Update a review            |
| DELETE | /api/v1/reviews/<review_id> | Delete a review            |
---
## Test Example
### Test User

```python

def test_user_creation(self):
        """Test successful User creation with valid data."""
        user = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
        self.assertEqual(user.first_name, "Alice")
        self.assertEqual(user.last_name, "Smith")
        self.assertEqual(user.email, "alice.smith@example.com")

```
### Test Amenity
```python
def test_amenity_creation_valid(self):
        amenity = Amenity(name="Wi-Fi")
        self.assertEqual(amenity.name, "Wi-Fi")
```
### Test Place
```python
 def test_create_place(self):
        r = self.create_place()
        self.assertEqual(r.status_code, 201)
        self.assertIn("id", r.json)
        self.assertEqual(r.json["owner_id"], self.user_id)
```
### Test review
```python
def test_create_review(self):
        """Test creating a review with valid data."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
```
---
## Key Concepts Applied
* *Modular Architecture:* Clear separation between API, business logic, and persistence.
* *Facade Pattern:* Simplifies communication between layers.
* *Flask-RESTx:* Used for structured API design and Swagger documentation.
* *Validation:* Ensures integrity of data and prevents invalid input.
* *Serialization:* Returns extended attributes (e.g., place owner details in place responses).
---
# Author
Wassef Abdallah

Warren Gomes Martins

Omar Rouigui