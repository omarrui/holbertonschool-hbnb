```mermaid
sequenceDiagram
participant Interface as Interface (User)
participant API as API (Presentation Layer)
participant UserModel as UserModel (Business Logic Layer)
participant UserRepository as UserRepository (Persistence Layer)
participant Database as Database
participant Mailer as EmailService

Interface ->> API: POST /UserRegistration {email, password, name}
API ->> UserModel: Validate fields
UserModel ->> UserModel: Normalize email (lower/trim)

alt VALIDATION FAILED
  UserModel -->> API: Validation error (details)
  API -->> Interface: 400 Bad Request
else VALIDATION SUCCESS
  API ->> UserModel: Create user request
  UserModel ->> UserRepository: Check uniqueness (email_lower)
  UserRepository ->> Database: SELECT * FROM users WHERE lower(email)=?
  Database -->> UserRepository: user|null

  alt E-MAIL EXISTS
    UserRepository -->> UserModel: Duplicate email
    UserModel -->> API: Conflict
    API -->> Interface: 409 Conflict
  else E-MAIL UNIQUE
    UserRepository -->> UserModel: Unique OK
    UserModel ->> UserModel: Hash password (argon2/bcrypt)
    UserModel ->> UserRepository: Save {email_lower, name, password_hash}
    UserRepository ->> Database: INSERT INTO users (...)
    Database -->> UserRepository: new user id

    alt UNIQUE CONSTRAINT VIOLATION (race)
      UserRepository -->> UserModel: Constraint error (duplicate)
      UserModel -->> API: Conflict
      API -->> Interface: 409 Conflict
    else INSERT OK
      UserRepository -->> UserModel: User persisted

      opt Email verification enabled
        UserModel ->> UserRepository: Issue verification token (TTL)
        UserRepository ->> Database: INSERT verification_token
        Database -->> UserRepository: token
        UserModel ->> Mailer: Send verification email (link)
        Mailer -->> UserModel: enqueued
      end

      opt Return access token on signup
        UserModel ->> UserModel: Issue JWT (access)
      end

      UserModel -->> API: User DTO (id, email, verified=false, maybe token)
      API -->> Interface: 201 Created
    end
  end
end