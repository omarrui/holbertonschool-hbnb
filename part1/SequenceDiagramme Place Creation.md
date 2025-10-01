```mermaid
sequenceDiagram
participant User
participant API
participant Auth
participant Service as PlaceService
participant DB as Database

User->>API: POST /places {...} + Bearer
API->>Auth: verify(jwt)

alt unauthorized
  Auth-->>API: invalid
  API-->>User: 401 Unauthorized
else authorized
  Auth-->>API: userId
  API->>Service: createPlace(userId, dto)

  alt invalid input
    Service-->>API: ValidationError
    API-->>User: 400 Bad Request
  else valid
    Service->>DB: INSERT INTO places (...)
    DB-->>Service: placeId | unique_violation

    alt unique violation
      Service-->>API: Conflict
      API-->>User: 409 Conflict
    else created
      Service-->>API: PlaceDTO(placeId, ...)
      API-->>User: 201 Created
    end
  end
end