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
