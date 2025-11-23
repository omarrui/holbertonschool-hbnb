# HolbertonBnB – RESTful API (Part 3)

### Authentication & Database Integration

A production-ready, **RESTful API** built with **Python**, **Flask-RESTX**, and **SQLAlchemy**, designed as the backend foundation of an Airbnb-like web application.
This version introduces **JWT-based authentication** and **persistent database storage** using **SQLite**.
It continues the modular architecture of Part 2 while enhancing **security**, **data durability**, and **user management**.

---

## Overview

The HolbertonBnB API now supports **secure authentication**, **role-based access control**, and **database integration**.
It implements full **CRUD** operations for **Users**, **Places**, **Amenities**, and **Reviews**, and stores data persistently using **SQLAlchemy ORM**.

All routes are **RESTful**, fully validated, and follow strict **error-handling** and **response formatting** standards.

---

## Features

### 🔐 Authentication

* **JWT Authentication** (login/logout with token validation)
* **Role-based access control** (admin / user)
* Securely hashed passwords
* Protected endpoints requiring valid tokens
* Automatic token expiration and refresh

### 🗄️ Database Persistence

* Migration from **in-memory storage** to **SQLite**
* Full integration with **SQLAlchemy ORM**
* Entity relationships:

  * One-to-Many: Users → Places / Reviews
  * Many-to-Many: Places ↔ Amenities
* Persistent data across sessions

### 🧱 Core CRUD Features

* Endpoints for **Users**, **Places**, **Amenities**, and **Reviews**
* Strict input validation
* Clear and consistent JSON responses
* Complete test coverage with `pytest` and `unittest`
* PEP8-compliant, no print statements or unnecessary logs

---

## Tech Stack

| Category       | Technology                   |
| -------------- | ---------------------------- |
| Language       | Python 3                     |
| Framework      | Flask, Flask-RESTX           |
| ORM & Database | SQLAlchemy + SQLite          |
| Authentication | Flask-JWT-Extended           |
| Testing        | unittest / pytest            |
| Architecture   | Facade + Repository patterns |
| Documentation  | Swagger / OpenAPI            |

---

## Project Structure

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
│   │       ├── auth.py
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

```bash
git clone https://github.com/<your-username>/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part3
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the database

```bash
python3 -c "from app import create_app; app = create_app(); app.app_context().push(); from app.models import db; db.create_all()"
```

### 5. Set environment variables

```bash
export FLASK_ENV=development
export JWT_SECRET_KEY=your-secret-key
export DATABASE_URL=sqlite:///hbnb_dev.db
```

### 6. Run the application

```bash
python3 run.py
```

The API will run locally at:
👉 **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**
Swagger UI is available at:
👉 **[http://127.0.0.1:5000/api/v1/](http://127.0.0.1:5000/api/v1/)**

---

## Core Entities

| Entity      | Description                                                                                                                              |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **User**    | Represents a platform user with authentication credentials and roles (admin/user). Passwords are hashed and never returned in responses. |
| **Place**   | Represents a property listed by a user. Includes attributes like name, price, location, and linked amenities.                            |
| **Amenity** | Represents a service or feature offered by a place (e.g., Wi-Fi, Pool).                                                                  |
| **Review**  | Represents user feedback on a place, with text, rating, and references to User and Place.                                                |

---

## Authentication Endpoints

| Method | Endpoint                | Description                    | Auth Required |
| ------ | ----------------------- | ------------------------------ | ------------- |
| POST   | `/api/v1/auth/register` | Register a new user            | ❌             |
| POST   | `/api/v1/auth/login`    | Log in and receive a JWT token | ❌             |
| POST   | `/api/v1/auth/logout`   | Log out (invalidate token)     | ✅             |
| GET    | `/api/v1/auth/profile`  | Get current user’s profile     | ✅             |

---

## API Endpoints Overview

### Users

| Method | Endpoint                  | Description             | Auth Required   |
| ------ | ------------------------- | ----------------------- | --------------- |
| POST   | `/api/v1/users/`          | Create a new user       | ❌               |
| GET    | `/api/v1/users/`          | List all users          | ✅ (Admin)       |
| GET    | `/api/v1/users/<user_id>` | Get user details        | ✅               |
| PUT    | `/api/v1/users/<user_id>` | Update user information | ✅ (Owner/Admin) |

---

### Amenities

| Method | Endpoint                         | Description                 | Auth Required |
| ------ | -------------------------------- | --------------------------- | ------------- |
| POST   | `/api/v1/amenities/`             | Create a new amenity        | ✅ (Admin)     |
| GET    | `/api/v1/amenities/`             | Retrieve all amenities      | ❌             |
| GET    | `/api/v1/amenities/<amenity_id>` | Retrieve a specific amenity | ❌             |
| PUT    | `/api/v1/amenities/<amenity_id>` | Update an amenity           | ✅ (Admin)     |

---

### Places

| Method | Endpoint                    | Description            | Auth Required |
| ------ | --------------------------- | ---------------------- | ------------- |
| POST   | `/api/v1/places/`           | Create a new place     | ✅             |
| GET    | `/api/v1/places/`           | Retrieve all places    | ❌             |
| GET    | `/api/v1/places/<place_id>` | Retrieve place details | ❌             |
| PUT    | `/api/v1/places/<place_id>` | Update a place         | ✅ (Owner)     |

---

### Reviews

| Method | Endpoint                      | Description          | Auth Required |
| ------ | ----------------------------- | -------------------- | ------------- |
| POST   | `/api/v1/reviews/`            | Create a review      | ✅             |
| GET    | `/api/v1/reviews/`            | Retrieve all reviews | ❌             |
| GET    | `/api/v1/reviews/<review_id>` | Retrieve a review    | ❌             |
| PUT    | `/api/v1/reviews/<review_id>` | Update a review      | ✅ (Owner)     |
| DELETE | `/api/v1/reviews/<review_id>` | Delete a review      | ✅ (Owner)     |

---

## Example Tests

### Authentication

```python
def test_login_valid_user(client):
    """Test logging in with valid credentials."""
    client.post('/api/v1/auth/register', json={
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "password": "secure123"
    })
    response = client.post('/api/v1/auth/login', json={
        "email": "alice@example.com",
        "password": "secure123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json
```

### Database Persistence

```python
def test_user_persistence(client):
    """Ensure user data persists in the SQLite database."""
    response = client.post('/api/v1/auth/register', json={
        "first_name": "Bob",
        "last_name": "Wilson",
        "email": "bob@example.com",
        "password": "secure123"
    })
    user_id = response.json["id"]

    response = client.get(f'/api/v1/users/{user_id}')
    assert response.status_code == 200
    assert response.json["email"] == "bob@example.com"
```

### CRUD Example

```python
def test_create_amenity_valid(client):
    """Test creating a new amenity."""
    response = client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
    assert response.status_code == 201
    assert response.json["name"] == "Wi-Fi"
```

---

## Key Concepts Applied

* **Modular Architecture** – clear separation between routes, services, and models
* **Authentication Layer** – secure JWT-based access control
* **ORM Integration** – persistence using SQLAlchemy
* **Facade Pattern** – simplifies communication between components
* **Validation & Serialization** – strict field validation and clean JSON output
* **Automated Testing** – full coverage with `pytest` and `unittest`

---

## Authors

**Wassef Abdallah**
**Warren Gomes Martins**
**Omar Rouigui**

*Holberton School – 2025-2026

---