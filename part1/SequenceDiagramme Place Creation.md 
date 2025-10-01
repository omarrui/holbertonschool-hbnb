```mermaid
sequenceDiagram
participant Interface as Interface (User)
participant API as API (Presentation Layer)
participant AuthService as AuthService (Business Logic Layer)
participant PlaceModel as PlaceModel (Business Logic Layer)
participant PlaceRepository as PlaceRepository (Persistence Layer)
participant Database as Database

Interface ->> API: POST /PlaceCreation {title, description, price, latitude, longitude}
API ->> AuthService: Validate token
AuthService ->> Database: Check token / get user (if session/blacklist)

alt INVALID TOKEN
  Database -->> AuthService: invalid / not found
  AuthService -->> API: unauthorized
  API -->> Interface: 401 Unauthorized (invalid token)
else VALID TOKEN
  Database -->> AuthService: OK (userId)
  AuthService -->> API: authenticated (userId)
  API ->> PlaceModel: Validate place fields

  alt VALIDATION FAILED
    PlaceModel -->> API: errors (details)
    API -->> Interface: 400 Bad Request (invalid fields)
  else VALIDATION SUCCESS
    PlaceModel ->> PlaceModel: business checks (price >= 0, latitude/longitude valid)
    API ->> PlaceModel: Create place (userId, dto)

    opt optional uniqueness (e.g., same owner + address/title)
      PlaceModel ->> PlaceRepository: existsByOwnerAndKey(userId, dto.key)
      PlaceRepository ->> Database: SELECT ... WHERE owner_id=? AND key=?
      Database -->> PlaceRepository: found|null
      alt duplicate found
        PlaceRepository -->> PlaceModel: duplicate
        PlaceModel -->> API: conflict
        API -->> Interface: 409 Conflict (duplicate place)
      else unique
        PlaceRepository -->> PlaceModel: ok
      end
    end

    PlaceModel ->> PlaceRepository: save(userId, dto)
    PlaceRepository ->> Database: INSERT INTO places (...)
    Database -->> PlaceRepository: new placeId

    alt UNIQUE CONSTRAINT VIOLATION (race)
      PlaceRepository -->> PlaceModel: constraint error (duplicate)
      PlaceModel -->> API: conflict
      API -->> Interface: 409 Conflict
    else INSERT OK
      PlaceRepository -->> PlaceModel: persisted (placeId)
      PlaceModel -->> API: place object (placeId, userId, fields)
      API -->> Interface: 201 Created {place}
    end
  end
end