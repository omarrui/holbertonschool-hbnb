# HBnB - UML Design Documentation

---

## Table of Contents
- [Project Overview](#project-overview)
- [Architecture Overview](#architecture-overview)
- [High-Level Package Diagram](#high-level-package-diagram)
- [Business Logic Layer](#business-logic-layer)
- [Entity Relationships](#entity-relationships)
- [Business Rules](#business-rules)
- [Design Decisions](#design-decisions)
- [Sequence Diagrams](#sequence-diagrams-for-api-calls)
- [Authors](#authors)

---

## Project Overview
This project contains comprehensive UML documentation for the HBnB (Holberton Airbnb) application. These diagrams serve as architectural blueprints before development begins and ensure consistency across database design and business logic implementation.

---

## Architecture Overview
The HBnB application follows a layered architecture pattern with clear separation of concerns:

- **Presentation Layer**: User interface and API endpoints  
- **Business Logic Layer**: Core entities and business rules  
- **Data Access Layer**: Database operations and persistence  

---

## High-Level Package Diagram
```mermaid
classDiagram
    class PresentationLayer {
        <<package>>
        UserController
        PlaceController
        ReviewController
        AmenityController
    }

    class BusinessLogicLayer {
        <<package>>
        UserClass
        PlaceClass
        ReviewClass
        AmenityClass
    }

    class PersistenceLayer {
        <<package>>
        UserData
        PlaceData
        ReviewData
        AmenityData
    }

    PresentationLayer --> BusinessLogicLayer : Facade Pattern
    BusinessLogicLayer --> PersistenceLayer : Database Operations
```

---

## Business Logic Layer

### Overview

The business logic layer contains the core domain entities that represent the fundamental concepts of our rental platform.

---

### Core Entities

#### User (ModelUser)

Represents platform users who can list properties and write reviews.

* **Key Attributes**: Unique identifier, personal information, authentication data
* **Capabilities**: Create, update, and delete user profiles
* **Security**: Password is private, admin status controls access levels

#### Place (ModelPlace)

Represents properties and their attributes.

* **Key Attributes**: Title, description, location, price, timestamps
* **Relationships**: Owned by a User, can have multiple reviews and amenities

#### Review (ModelReview)

Represents user feedback and ratings for places.

* **Key Attributes**: Rating, comment, timestamps
* **Relationships**: Written by a User for a specific Place

#### Amenity (ModelAmenity)

Represents facilities and services available at places.

* **Key Attributes**: Name, description, management timestamps
* **Relationship**: Many-to-many with Places via ModelPlaceAmenity

#### PlaceAmenity (ModelPlaceAmenity)

Junction table managing the many-to-many relationship between Places and Amenities.

---

### Class Diagram

```mermaid
classDiagram
direction LR
    class ModelUser {
        +UUID4 id
        +str first_name
        +str last_name
        +str email
        -str password
        -bool is_admin
        +datetime created_at
        +datetime updated_at
        +create_user()
        +update_user()
        +delete_user()
    }

    class ModelPlace {
        +UUID4 id
        +UUID4 user_id
        +str title
        +str description
        +float price
        +float latitude
        +float longitude
        +datetime created_at
        +datetime updated_at
        +create_place()
        +update_place()
        +delete_place()
        +list_reviews()
        +list_amenities()
    }

    class ModelReview {
        +UUID4 id
        +UUID4 user_id
        +UUID4 place_id
        +int rating
        +str comment
        +datetime created_at
        +datetime updated_at
        +create_review()
        +update_review()
        +delete_review()
    }

    class ModelAmenity {
        +UUID4 id
        +str name
        +str description
        +datetime created_at
        +datetime updated_at
        +create_amenity()
        +update_amenity()
        +delete_amenity()
    }

    class ModelPlaceAmenity {
        +UUID4 id
        +UUID4 place_id
        +UUID4 amenity_id
    }

    ModelUser "1" o-- "0..*" ModelPlace : owns
    ModelUser "1" o-- "0..*" ModelReview : writes
    ModelPlace "1" --> "0..*" ModelReview : has
    ModelPlace "1" --> "0..*" ModelPlaceAmenity : contains
    ModelAmenity "1" --> "0..*" ModelPlaceAmenity : linked_to
```

---

## Entity Relationships

* **User -> Place**: One-to-Many (1:0..*)
* **Place -> Review**: One-to-Many (1:0..*)
* **Place <-> Amenity**: Many-to-Many (via PlaceAmenity)

---

## Business Rules

* Only authenticated users can create places or reviews
* Users cannot review their own properties
* Referential integrity must be maintained for all foreign keys
* Amenities can be shared across multiple places

---

## Design Decisions

* **UUID4** for all primary keys
* Automatic timestamps for creation and update
* Integer coordinates for latitude/longitude
* Integer rating scale (1–5)
* Future considerations: soft delete, audit trails, rating validation

---

## Sequence Diagrams for API Calls

### User Registration

```mermaid
sequenceDiagram
participant User
participant API
participant UserService
participant UserRepository
participant Database

User->>API: POST /users {email, password, name}
API->>UserService: validateAndProcess(dto)
alt invalid input
  UserService-->>API: ValidationError
  API-->>User: 400 Bad Request
else valid
  UserService->>Database: check if email exists
  alt email exists
    UserService-->>API: Conflict
    API-->>User: 409 Conflict
  else create
    UserService->>Database: INSERT new user
    Database-->>UserService: new user id
    UserService-->>API: user DTO
    API-->>User: 201 Created
  end
end
```

### Place Creation

```mermaid
sequenceDiagram
participant User
participant API
participant Auth
participant PlaceService
participant Database

User->>API: POST /places {...} + Bearer
API->>Auth: verify(jwt)
alt unauthorized
  Auth-->>API: invalid
  API-->>User: 401 Unauthorized
else authorized
  Auth-->>API: userId
  API->>PlaceService: createPlace(userId, dto)
  alt invalid input
    PlaceService-->>API: ValidationError
    API-->>User: 400 Bad Request
  else valid
    PlaceService->>Database: INSERT INTO places
    Database-->>PlaceService: placeId
    PlaceService-->>API: PlaceDTO
    API-->>User: 201 Created
  end
end
```

### Review Submission

```mermaid
sequenceDiagram
participant User
participant ReviewController
participant ReviewService
participant ReviewRepository

User->>ReviewController: Submit Review (POST /reviews)
ReviewController->>ReviewService: Validate and process review
ReviewService->>ReviewRepository: Save review to database
ReviewRepository-->>ReviewService: Confirm save
ReviewService-->>ReviewController: Return processed review
ReviewController-->>User: Return success response
```

### Fetching a List of Places

```mermaid
sequenceDiagram
participant User
participant PlaceController
participant PlaceService
participant PlaceRepository

User->>PlaceController: Request list of places (GET /places)
PlaceController->>PlaceService: Fetch places
PlaceService->>PlaceRepository: Retrieve places from database
PlaceRepository-->>PlaceService: Return places
PlaceService-->>PlaceController: Send places
PlaceController-->>User: Return places list
```

---

## Authors

Omar, Warren, Wassef

```

