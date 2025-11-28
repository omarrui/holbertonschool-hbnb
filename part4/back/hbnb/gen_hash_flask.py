from app import bcrypt
password = 'admin1234'
hashed = bcrypt.generate_password_hash(password).decode('utf-8')
print(hashed)
