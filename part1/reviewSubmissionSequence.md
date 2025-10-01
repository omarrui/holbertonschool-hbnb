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
