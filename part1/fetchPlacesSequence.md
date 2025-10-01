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
