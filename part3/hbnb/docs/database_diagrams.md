# HBnB — Diagramme database

Ce fichier contient le diagramme représentant le schéma de base de données principal du projet HBnB : User, Place, Review, Amenity et la table de jointure Place_Amenity.

```mermaid
erDiagram
    USER {
        string id PK
        string first_name
        string last_name
        string email
        string password
        boolean is_admin
    }

    PLACE {
        string id PK
        string title
        string description
        float price
        float latitude
        float longitude
        string owner_id FK
    }

    REVIEW {
        string id PK
        string text
        int rating
        string user_id FK
        string place_id FK
    }

    AMENITY {
        string id PK
        string name
    }

    PLACE_AMENITY {
        string place_id FK 
        string amenity_id FK
    }

    %% Relations
    USER ||--o{ PLACE : "owns"
    USER ||--o{ REVIEW : "writes"
    PLACE ||--o{ REVIEW : "has"

    %% Many-to-many via join table
    PLACE ||--o{ PLACE_AMENITY : "has"
```
