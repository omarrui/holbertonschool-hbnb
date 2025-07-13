# HBnB Project – Part 3: Database Integration with SQLAlchemy

## 📚 Overview

This project is part of the HBnB application at Holberton School.  
Part 3 focuses on integrating a **SQLAlchemy database** with the existing Flask application, replacing the in-memory repository with persistent data storage.

The goal of this part is to:
- Integrate SQLAlchemy ORM for database operations
- Implement proper database models with relationships
- Add JWT authentication and authorization
- Maintain API functionality with persistent data storage
- Ensure data validation and error handling

---

## 🗂️ Project Structure

```
part3/
├── app/
│   ├── __init__.py                 # Flask app initialization
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py            # User API endpoints
│   │       ├── places.py           # Place API endpoints
│   │       ├── reviews.py          # Review API endpoints
│   │       ├── amenities.py        # Amenity API endpoints
│   │       ├── auth.py             # Authentication endpoints
│   │       └── protected.py        # Protected routes
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py                 # Base model with SQLAlchemy
│   │   ├── user.py                 # User model
│   │   ├── place.py                # Place model
│   │   ├── review.py               # Review model
│   │   └── amenity.py              # Amenity model
│   ├── services/
│   │   ├── __init__.py
│   │   └── facade.py               # Facade layer
│   └── persistence/
│       ├── __init__.py
│       └── repository.py           # SQLAlchemy repository
├── hbnb/
│   ├── config.py                   # App configuration
│   ├── requirements.txt            # Project dependencies
│   ├── run.py                      # App entry point
│   ├── create_admin.py             # Admin user creation script
│   ├── test_user.py                # User tests
│   ├── test_place.py               # Place tests
│   ├── test_all.py                 # Comprehensive tests
│   ├── app/
│   │   ├── __init__.py
│   │   ├── extensions.py           # Flask extensions
│   │   ├── models/                 # Database models
│   │   ├── api/                    # API routes
│   │   ├── services/               # Business logic
│   │   └── persistence/            # Data access layer
│   ├── instance/
│   │   └── development.db          # SQLite database
│   ├── schema/
│   │   ├── creation_tables.sql     # Database schema
│   │   └── inserting_data.sql      # Sample data
│   └── diagram/
│       └── er_diagram.mmd          # Entity-Relationship diagram
└── README.md                       # This file
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.8+
- pip (Python package installer)
- SQLite3 (comes with Python)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/omarrui/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part3/hbnb

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python create_admin.py

# Run the application
python run.py
```

### 3. Access the Application

- **API Documentation**: http://localhost:5000/
- **Base URL**: http://localhost:5000/api/v1/
- **Database**: SQLite file at `instance/development.db`

---

## 🛠️ Tech Stack

- **Python 3.8+**: Programming language
- **Flask**: Web framework
- **Flask-RESTx**: RESTful API framework with Swagger documentation
- **SQLAlchemy**: ORM for database operations
- **Flask-JWT-Extended**: JWT authentication
- **Flask-Bcrypt**: Password hashing
- **SQLite**: Database (development)
- **Unittest**: Testing framework

---

## 🗃️ Database Schema

### Users Table
- `id`: Primary key (UUID)
- `first_name`: User's first name
- `last_name`: User's last name
- `email`: Unique email address
- `password`: Hashed password
- `is_admin`: Admin privileges flag
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Places Table
- `id`: Primary key (UUID)
- `title`: Place title
- `description`: Place description
- `price`: Price per night
- `latitude`: Geographic latitude
- `longitude`: Geographic longitude
- `owner_id`: Foreign key to Users
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Reviews Table
- `id`: Primary key (UUID)
- `text`: Review text
- `rating`: Rating (1-5)
- `user_id`: Foreign key to Users
- `place_id`: Foreign key to Places
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Amenities Table
- `id`: Primary key (UUID)
- `name`: Amenity name
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Place-Amenity Association Table
- `place_id`: Foreign key to Places
- `amenity_id`: Foreign key to Amenities

---

## 🔐 Authentication

### JWT Token Authentication

The API uses JWT tokens for authentication:

1. **Login**: POST `/api/v1/auth/login`
2. **Protected Routes**: Include `Authorization: Bearer <token>` header
3. **Admin Routes**: Require admin privileges

### Example Usage

```bash
# Login
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hbnb.io", "password": "admin123"}'

# Use token in protected routes
curl -X GET http://localhost:5000/api/v1/protected/admin-only \
  -H "Authorization: Bearer <your-jwt-token>"
```

---

## 📡 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/protected/admin-only` - Admin-only endpoint

### Users
- `GET /api/v1/users/` - List all users
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

### Places
- `GET /api/v1/places/` - List all places
- `POST /api/v1/places/` - Create a new place
- `GET /api/v1/places/{id}` - Get place by ID
- `PUT /api/v1/places/{id}` - Update place
- `DELETE /api/v1/places/{id}` - Delete place
- `GET /api/v1/places/{id}/reviews` - Get reviews for a place

### Reviews
- `GET /api/v1/reviews/` - List all reviews
- `POST /api/v1/reviews/` - Create a new review
- `GET /api/v1/reviews/{id}` - Get review by ID
- `PUT /api/v1/reviews/{id}` - Update review
- `DELETE /api/v1/reviews/{id}` - Delete review

### Amenities
- `GET /api/v1/amenities/` - List all amenities
- `POST /api/v1/amenities/` - Create a new amenity
- `GET /api/v1/amenities/{id}` - Get amenity by ID
- `PUT /api/v1/amenities/{id}` - Update amenity
- `DELETE /api/v1/amenities/{id}` - Delete amenity

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m unittest discover -s . -p "test_*.py"

# Run specific test files
python -m unittest test_user.py
python -m unittest test_place.py
python -m unittest test_all.py

# Run tests with verbose output
python -m unittest -v test_all.py
```

### Test Coverage

#### test_user.py
- User creation with valid/invalid data
- User retrieval (all users, by ID)
- User updates and validation
- Duplicate email handling
- Invalid email format handling

#### test_place.py
- Place creation with valid/invalid data
- Place retrieval and updates
- Place deletion
- Amenity associations
- Owner validation
- Geographic coordinate validation

#### test_all.py
- Comprehensive API testing
- CRUD operations for all entities
- Error handling and edge cases
- Authentication testing
- Data validation
- Relationship integrity

---

## 🧠 Key Features

### Database Integration
- **SQLAlchemy ORM**: Full database integration replacing in-memory storage
- **Migrations**: Database schema versioning
- **Relationships**: Proper foreign key relationships between entities
- **Validation**: Data validation at model level

### Security
- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt for secure password storage
- **Admin Privileges**: Role-based access control
- **Input Validation**: Comprehensive input validation

### API Features
- **RESTful Design**: Following REST principles
- **Swagger Documentation**: Auto-generated API documentation
- **Error Handling**: Consistent error responses
- **CORS Support**: Cross-origin resource sharing

### Data Models
- **Base Model**: Common fields and methods for all entities
- **User Model**: User management with authentication
- **Place Model**: Property listings with geographic data
- **Review Model**: User reviews with ratings
- **Amenity Model**: Property amenities with many-to-many relationships

---

## 📝 Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=sqlite:///instance/development.db

# JWT
JWT_SECRET_KEY=your-secret-key-here

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
```

### Database Configuration

```python
# config.py
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
```

---

## 🔧 Development

### Adding New Features

1. **Create Model**: Add new model in `app/models/`
2. **Create Repository**: Add repository methods in `app/persistence/`
3. **Update Facade**: Add business logic in `app/services/facade.py`
4. **Create API**: Add endpoints in `app/api/v1/`
5. **Write Tests**: Add comprehensive tests

### Code Style

- Follow PEP8 standards
- Use type hints where appropriate
- Document all functions and classes
- Write comprehensive tests

---

## 📊 Performance Considerations

- **Database Indexing**: Indexes on frequently queried fields
- **Query Optimization**: Efficient SQLAlchemy queries
- **Caching**: Future implementation for frequently accessed data
- **Pagination**: Large result set handling

---

## 🚀 Deployment

### Production Considerations

1. **Database**: Use PostgreSQL or MySQL for production
2. **Environment**: Set proper environment variables
3. **Security**: Use strong JWT secret keys
4. **Logging**: Implement comprehensive logging
5. **Monitoring**: Add application monitoring

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

---

## 📞 Support

For questions or issues:
- Check the API documentation at `/`
- Review the test files for usage examples
- Check the database schema in `schema/`

---

## 📄 License

This project is part of the Holberton School curriculum.

---

## 👥 Authors

**Omar Rouigui & Herve Riche**

GitHub: @omarrui

---

## 🔄 Version History

- **Part 1**: Basic project structure
- **Part 2**: In-memory repository with Flask-RESTx
- **Part 3**: SQLAlchemy database integration with JWT authentication

---

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-RESTx Documentation](https://flask-restx.readthedocs.io/)
- [JWT Documentation](https://jwt.io/)

