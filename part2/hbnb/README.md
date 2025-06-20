# HBnB Project – Part 2: Project Setup & Initialization

## 📚 Overview

This project is part of the HBnB application at Holberton School.  
It focuses on setting up a modular Flask application with clean separation of concerns using the **Facade design pattern** and an **in-memory repository**.

The goal of this part is to:
- Organize the project into proper layers (API, Models, Services, Persistence)
- Set up a basic Flask app structure with versioned routing
- Prepare for future database integration using SQLAlchemy

---

## 🗂️ Project Structure
hbnb/
├── app/
│   ├── init.py                 # Flask app initialization
│   ├── api/                        # API layer (Flask routes)
│   │   ├── init.py
│   │   └── v1/
│   │       ├── init.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── amenities.py
│   ├── models/                     # Data models / business logic
│   │   ├── init.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── services/                   # Facade layer (connects logic to persistence)
│   │   ├── init.py
│   │   └── facade.py
│   └── persistence/               # In-memory data handling
│       ├── init.py
│       └── repository.py
├── config.py                       # App configuration
├── requirements.txt                # Project dependencies
├── run.py                          # App entry point
└── README.md                       # This file
---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/omarrui/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part2

Install dependencies
    pip install -r requirements.txt

Run the application
    python run.py

🧠 Key Concepts
	•	Flask: Lightweight web framework for Python
	•	Flask-RESTx: Helps build RESTful APIs with documentation
	•	Facade Pattern: Simplifies interactions between layers
	•	In-Memory Repository: Temporary data storage before DB integration

⸻

🛠️ Tech Stack
	•	Python3
	•	Flask
	•	Flask-RESTx
    .   venv

⸻

📌 Notes
	•	The current repository uses in-memory data storage.
	•	In later parts of the project, this will be replaced with SQLAlchemy and a real daabase.
	•	No routes are functional yet – they’ll be added in future tasks.

🧪 Testing
Running Tests
To run the test suite, use the following command:

"
python -m unittest discover -s part2/hbnb -p "test_*.py"
"

Test Files Overview

test_user.py
	Purpose: Tests all user-related functionality.
	What it Covers:
		Creating a User:
			Tests the POST /api/v1/users/ endpoint to ensure users can be created with valid data.
			Handles invalid input (e.g., missing fields, invalid email format).
		Retrieving Users:
			Tests the GET /api/v1/users/ endpoint to retrieve all users.
			Tests the GET /api/v1/users/<user_id> endpoint to retrieve a user by ID.
			Handles cases where the user does not exist.
		Updating a User:
			Tests the PUT /api/v1/users/<user_id> endpoint to update user details.
			Verifies that the updates are applied correctly.
		Special Cases:
			Tests creating a user with duplicate emails.
			Tests creating a user with invalid email formats.

test_place.py
	Purpose: Tests all place-related functionality.
	What it Covers:
		Creating a Place:
			Tests the POST /api/v1/places/ endpoint to ensure places can be created with valid data.
			Handles invalid input (e.g., missing fields, invalid owner ID).
		Retrieving Places:
			Tests the GET /api/v1/places/ endpoint to retrieve all places.
			Tests the GET /api/v1/places/<place_id> endpoint to retrieve a specific place.
			Handles cases where the place does not exist.
		Updating a Place:
			Tests the PUT /api/v1/places/<place_id> endpoint to update place details.
			Verifies that the updates are applied correctly.
		Deleting a Place:
			Tests the DELETE /api/v1/places/<place_id> endpoint to delete a place.
			Verifies that the place is no longer retrievable after deletion.
		Special Cases:
			Tests creating a place with amenities.
			Tests creating a place with invalid latitude, longitude, or price values.
			Tests creating a place with missing required fields.

test_all.py
	Purpose: A comprehensive test suite that covers all aspects of the API, including users, places, amenities, and reviews.
	What it Covers:
		Setup:
			Creates test data for users, places, amenities, and reviews.
			Ensures valid test data is available for all tests.
		Create Operations:
			Tests creating users, places, amenities, and reviews with valid data.
			Handles invalid data (e.g., missing fields, invalid formats).
		Retrieve Operations:
			Tests retrieving all entities (users, places, amenities, reviews).
			Tests retrieving entities by ID.
			Handles cases where the entity does not exist.
		Update Operations:
			Tests updating entities with valid data.
			Handles invalid data (e.g., invalid email, invalid latitude/longitude).
			Handles cases where the entity does not exist.
		Delete Operations:
			Tests deleting entities (e.g., reviews).
		Special Conditions:
			Tests edge cases, such as:
				Duplicate emails.
				Invalid latitude/longitude for places.
				Zero or negative ratings for reviews.
				Updating entities with non-existent IDs.


How to Run Specific Tests
	To run a specific test file, use:

		python -m unittest test_user.py
	or
		python -m unittest test_place.py
	or
		python -m unittest test_all.py


👥 Authors

	Omar Rouigui & Herve 
	
	GitHub: @omarrui

