-- =============================
-- HBnB Database Schema
-- =============================

DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS users;

-- -----------------------------
-- User Table
-- -----------------------------
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------
-- Place Table
-- -----------------------------
CREATE TABLE places (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- -----------------------------
-- Review Table
-- -----------------------------
CREATE TABLE reviews (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    UNIQUE (user_id, place_id)
);

-- -----------------------------
-- Amenity Table
-- -----------------------------
CREATE TABLE amenities (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------
-- Place_Amenity Table (Many-to-Many)
-- -----------------------------
CREATE TABLE place_amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);
-- =============================
-- HBnB Initial Data
-- =============================

-- Insert administrator user
INSERT OR REPLACE INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at) VALUES 
('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$5VkrO9ikT3ppdKqJUiI35u8GWxei6AMB/Zxa9xTZYdrfzpYkbi/MK', TRUE, datetime('now'), datetime('now'));

-- Insert initial amenities
INSERT INTO amenities (id, name, created_at, updated_at) VALUES 
('550e8400-e29b-41d4-a716-446655440001', 'WiFi', datetime('now'), datetime('now')),
('550e8400-e29b-41d4-a716-446655440002', 'Swimming Pool', datetime('now'), datetime('now')),
('550e8400-e29b-41d4-a716-446655440003', 'Air Conditioning', datetime('now'), datetime('now'));
