```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic as UserService
participant Database

User->>API: POST /users {email, password, name}
API->>BusinessLogic: validateAndProcess(dto)

alt invalid input
  BusinessLogic-->>API: ValidationError
  API-->>User: 400 Bad Request
else valid
  BusinessLogic->>Database: SELECT id FROM users WHERE lower(email)=?
  Database-->>BusinessLogic: user|null

  alt email exists
    BusinessLogic-->>API: Conflict
    API-->>User: 409 Conflict
  else create
    BusinessLogic->>BusinessLogic: normalize email + hash password
    BusinessLogic->>Database: INSERT INTO users (...)
    Database-->>BusinessLogic: new user id

    alt UNIQUE constraint violation (race)
      BusinessLogic-->>API: Conflict
      API-->>User: 409 Conflict
    else ok
      opt Email verification / token
        BusinessLogic->>BusinessLogic: issue verification token / JWT
      end
      BusinessLogic-->>API: user DTO (id, email, verified=false, maybe token)
      API-->>User: 201 Created
    end
  end
end