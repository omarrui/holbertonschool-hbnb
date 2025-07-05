-- Insert Admin User
INSERT INTO users (id, email, first_name, last_name, password, is_admin)
VALUES (
  '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
  'admin@hbnb.io',
  'Admin',
  'HBnB',
  '$2b$12$LfIfTefU5/xkyWjd0x.j5Om0tYZhukaYfUvGbGkVuY2.DgtnmJ.l.',  -- bcrypt2 hashed password
  TRUE
);

-- Insert Amenities
INSERT INTO amenities (id, name) VALUES
('5e8b42ce-9bd1-40e6-a8df-0beeb9482896', 'WiFi'),
('e2a69cf0-0241-4c1a-9d4d-88d372c0a401', 'Swimming Pool'),
('d5af72a2-0d61-4b3f-bae2-0cf85868a4ef', 'Air Conditioning');