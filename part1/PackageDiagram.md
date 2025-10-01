```mermaid
classDiagram
    class PresentationLayer {
	    +UserController
	    +PlaceController
	    +ReviewController
	    +AmenityController
    }

    class BusinessLogicLayer {
	    +User
	    +Place
	    +Review
	    +Amenity
    }

    class PersistenceLayer {
	    +UserDatabase
	    +PlaceDatabase
	    +ReviewDatabase
	    +AmenityDatabase
    }

    PresentationLayer --> BusinessLogicLayer : Facade Pattern
    BusinessLogicLayer --> PersistenceLayer : Database Operations
