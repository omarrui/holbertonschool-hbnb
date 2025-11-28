-- =============================
-- Initial Data for HBnB Database
-- =============================

-- Admin user
REPLACE INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$/RZ2MjB6nbcpA6Std60Odu058SPgmKMhfIinpmadLtSBYcyIqR8/2', -- bcrypt hash for 'admin1234'
    TRUE,
    datetime('now'),
    datetime('now')
);

-- -- Initial amenities
-- INSERT INTO amenities (id, name)
-- VALUES
--     ('7e53769f-d9c5-4c45-8d32-0f2aaf3d43b2', 'WiFi'),
--     ('f94b5a28-9326-4ee2-a49b-5b9b38ef154e', 'Swimming Pool'),
--     ('c23f1a18-bc15-4a63-a7fd-2d79c6e43b1c', 'Air Conditioning');
