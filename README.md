🏡 AirBnB Clone Project

A full-stack web application that emulates the core features of Airbnb. This project showcases a layered architecture with a clean separation of concerns, allowing users to register, manage listings, and book accommodations securely and intuitively.

⸻

📁 Files Included
	•	ClassDiagram.mmd
	•	PackageDiagram.mmd
	•	README.md
	•	SequenceDiagramUserRegistration.mmd
	•	SequenceDiagramPlaceManagement.mmd
	•	SequenceDiagramPlaceCreation.mmd
	•	SequenceDiagramReviewSubmission.mmd

⸻

⚙️ Architecture Overview

This project follows a three-tier layered architecture:
classDiagram

class PresentationLayer {
    +UserController
    +PlaceController
    +ReviewController
    +AmenityController
    +WebServices
    +ClientUI
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

PresentationLayer --> BusinessLogicLayer : Facade Pattern (Service Interface)
BusinessLogicLayer --> PersistenceLayer : Data Access Operations

classDiagram

class PresentationLayer {
    +UserController
    +PlaceController
    +ReviewController
    +AmenityController
    +WebServices
    +ClientUI
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

PresentationLayer --> BusinessLogicLayer : Facade Pattern (Service Interface)
BusinessLogicLayer --> PersistenceLayer : Data Access Operations