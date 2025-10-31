-- =============================
-- Initial Data for HBnB Database
-- =============================

-- Admin user
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$Nf4t7Icfk9JQK9p8AvZV8u4FA3DkZ3pGzS8z5iG4Cl9EcnM1IjBfa', -- bcrypt hash for 'admin1234'
    TRUE
);

-- Initial amenities
INSERT INTO amenities (id, name)
VALUES
    ('7e53769f-d9c5-4c45-8d32-0f2aaf3d43b2', 'WiFi'),
    ('f94b5a28-9326-4ee2-a49b-5b9b38ef154e', 'Swimming Pool'),
    ('c23f1a18-bc15-4a63-a7fd-2d79c6e43b1c', 'Air Conditioning');
