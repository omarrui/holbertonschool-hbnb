# HBnB Project – Technical Documentation

## Introduction

This document serves as the comprehensive technical blueprint for the HBnB project, a web-based rental booking platform inspired by Airbnb. It compiles all architectural diagrams and explanatory notes, providing a clear reference for the system’s design and guiding the implementation phases. The document covers the high-level architecture, business logic, and detailed API interaction flows.

---

## 1. High-Level Architecture

### Package Diagram

```mermaid
classDiagram

class PresentationLayer {
    +UserController
    +PlaceController
    +ReviewController
    +AmenityController
    +WebServices
}

class BusinessLogicLayer {
    +UserManager
    +PlaceManager
    +ReviewManager
    +AmenityManager
}

class PersistenceLayer {
    +UserDAO
    +PlaceDAO
    +ReviewDAO
    +AmenityDAO
    +DatabaseConnection
}

PresentationLayer --> BusinessLogicLayer : Facade Pattern (Interface)
BusinessLogicLayer --> PersistenceLayer : Data Access
```

#### Explanatory Notes

- **Purpose:** This diagram illustrates the overall layered architecture of the HBnB system.
- **Key Components:**
  - **PresentationLayer:** Handles HTTP requests, user input, and API endpoints.
  - **BusinessLogicLayer:** Contains core business rules and logic, exposed via a facade.
  - **PersistenceLayer:** Manages data storage and retrieval, abstracting the database.
- **Design Decisions:**
  - **Layered Approach:** Promotes separation of concerns, maintainability, and testability.
  - **Facade Pattern:** The PresentationLayer interacts with the BusinessLogicLayer through a unified interface, simplifying API design and decoupling layers.
- **Role in Architecture:** This structure ensures that each layer has a clear responsibility, making the system modular and scalable.

---

## 2. Business Logic Layer

### Class Diagram

```mermaid
classDiagram
class BaseModel {
    + UUID id
    + DateTime createdAt
    + DateTime updatedAt
}

class User {
    + string firstName
    + string lastName
    + string email
    + string password
    + bool isAdmin
    + register()
    + updateProfile()
    + deleteAccount()
    + setAdmin()
}

class Place {
    + string title
    + string description
    + float price
    + float latitude
    + float longitude
    + UUID hostId
    + create()
    + update()
    + delete()
    + getAll()
}

class Review {
    + UUID userId
    + UUID placeId
    + int rating
    + string comment
    + add()
    + edit()
    + delete()
    + getByPlace()
}

class Amenity {
    + string name
    + string details
    + add()
    + update()
    + delete()
    + listAll()
}

BaseModel <|-- User
BaseModel <|-- Place
BaseModel <|-- Review
BaseModel <|-- Amenity

User "1" *-- "0..*" Place : owns
Place "1" *-- "0..*" Review : receives
Place "0..*" *-- "0..*" Amenity : includes
User "1" *-- "0..*" Review : writes
```

#### Explanatory Notes

- **Purpose:** Details the main entities and their relationships in the business logic layer.
- **Key Components:**
  - **BaseModel:** Provides common fields (`id`, `createdAt`, `updatedAt`) for all entities.
  - **User:** Represents platform users, including admin status and authentication methods.
  - **Place:** Represents rental listings, linked to an owner (User) and amenities.
  - **Review:** Represents user feedback on places, linked to both User and Place.
  - **Amenity:** Represents features available at a place.
- **Design Decisions:**
  - **Inheritance:** All entities inherit from `BaseModel` for consistency.
  - **Associations:** Relationships (e.g., User owns Places, Place has Reviews) are explicitly modeled for clarity and data integrity.
- **Role in Architecture:** This diagram guides the implementation of the core business logic and data models.

---

## 3. API Interaction Flow

### Sequence Diagrams

#### 3.1 User Registration

```mermaid
sequenceDiagram
participant Client
participant FrontendLayer
participant ServiceLayer
participant DataLayer

Client->>FrontendLayer: Submit registration form
FrontendLayer->>ServiceLayer: Passes data for processing
ServiceLayer-->>ServiceLayer: Validates user input

alt Invalid Input
    ServiceLayer-->>FrontendLayer: Return error response
    FrontendLayer-->>Client: Show error message
else Valid Input
    ServiceLayer->>DataLayer: Store new user in database
    DataLayer-->>ServiceLayer: Acknowledge success
    ServiceLayer-->>FrontendLayer: Confirmation response
    FrontendLayer-->>Client: Display success message
end
```

**Notes:**  
- Shows the flow from user registration request to database persistence.
- Validation is handled in the ServiceLayer; errors are returned immediately if input is invalid.

---

#### 3.2 Place Creation

```mermaid
sequenceDiagram
participant Host
participant FrontendLayer
participant ServiceLayer
participant DataLayer
participant Logger

Host->>FrontendLayer: Submit new place info
FrontendLayer->>ServiceLayer: Forward creation request
ServiceLayer-->>ServiceLayer: Validate place data

alt All data valid
    ServiceLayer->>DataLayer: Save place in DB
    ServiceLayer->>Logger: Log place creation
    Logger-->>ServiceLayer: Log saved
    DataLayer-->>ServiceLayer: Success confirmation
    ServiceLayer-->>FrontendLayer: Place created successfully
    FrontendLayer-->>Host: Show confirmation
else Validation failed
    ServiceLayer-->>FrontendLayer: Return error details
    FrontendLayer-->>Host: Show form errors
end
```

**Notes:**  
- Demonstrates the process for creating a new place, including validation and logging.
- Ensures that only valid data is persisted and that actions are auditable.

---

#### 3.3 Place Listing (Search)

```mermaid
sequenceDiagram
participant User
participant FrontendLayer
participant ServiceLayer
participant DataLayer

User->>FrontendLayer: Search for places with filters
FrontendLayer->>ServiceLayer: Handle request
ServiceLayer-->>ServiceLayer: Check search params
ServiceLayer->>DataLayer: Query matching places

DataLayer->>DataLayer: Execute SQL/filter logic
DataLayer-->>ServiceLayer: Return results
ServiceLayer-->>FrontendLayer: Format and filter results
FrontendLayer-->>User: Display place listings
```

**Notes:**  
- Illustrates how search requests are processed, validated, and fulfilled.
- The ServiceLayer ensures only valid queries reach the DataLayer.

---

#### 3.4 Review Submission

```mermaid
sequenceDiagram
participant User
participant FrontendLayer
participant ServiceLayer
participant DataLayer
participant Logger

User->>FrontendLayer: Submit review with rating/comment
FrontendLayer->>ServiceLayer: Send review request
ServiceLayer-->>ServiceLayer: Validate input

alt Passed
    ServiceLayer->>DataLayer: Store review
    DataLayer->>Logger: Record review action
    Logger-->>DataLayer: Log confirmed
    DataLayer-->>ServiceLayer: Success
    ServiceLayer-->>FrontendLayer: Review accepted
    FrontendLayer-->>User: Show confirmation
else Failed
    ServiceLayer-->>FrontendLayer: Return validation error
    FrontendLayer-->>User: Display error
end
```

**Notes:**  
- Captures the review creation process, including validation and audit logging.
- Ensures traceability and data integrity for user-generated content.

---

## Conclusion

This technical document provides a unified and detailed view of the HBnB project’s architecture, business logic, and API flows. The diagrams and explanations herein serve as a reference for developers and stakeholders, ensuring a shared understanding and a solid foundation for implementation and future enhancements.
