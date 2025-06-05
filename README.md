# AirBnB Clone – Full-Stack Project

A web-based platform that mimics the key features of Airbnb. This project showcases a complete web application built with a layered architecture and clean separation of concerns. Users can sign up, browse listings, book places, and leave reviews.

## Project Objective

To develop a responsive, intuitive, and functional rental booking system where users can create, explore, and manage accommodations. The system includes authentication, listing management, reviews, and amenity features.

---

## 📁 Project Files

- [`ClassDiagram.mmd`](./ClassDiagram.mmd)
- [`PackageDiagram.mmd`](./PackageDiagram.mmd)
- [`SequenceDiagram_UserRegistration.mmd`](./SequenceDiagram_UserRegistration.mmd)
- [`SequenceDiagram_PlaceCreation.mmd`](./SequenceDiagram_PlaceCreation.mmd)
- [`SequenceDiagram_PlaceListing.mmd`](./SequenceDiagram_PlaceListing.mmd)
- [`SequenceDiagram_ReviewSubmission.mmd`](./SequenceDiagram_ReviewSubmission.mmd)

---

## 🧱 Architecture Overview

This system is structured using a **three-layer architecture** for modularity and clarity.

```mermaid
classDiagram

class FrontendLayer {
    +UserController
    +PlaceController
    +ReviewController
    +AmenityController
    +WebAppUI
}

class ServiceLayer {
    +UserService
    +PlaceService
    +ReviewService
    +AmenityService
}

class DataLayer {
    +UserRepo
    +PlaceRepo
    +ReviewRepo
    +AmenityRepo
    +DBConnection
}

FrontendLayer --> ServiceLayer : Calls Services
ServiceLayer --> DataLayer : Interacts with DB

🧩 Data Model

The structure of the application’s entities is as follows:
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

  ⚙️ Key Functionalities:
  

  🧾 User Registration
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


🏡 Place Creation
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


🔍 Place Listing
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


📝 Review Submission
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


🛠️ Technologies Used
(nothing yet)


👨‍💻 Authors
	•	Omar Rouigui
	•	Hervé Le Guennec
