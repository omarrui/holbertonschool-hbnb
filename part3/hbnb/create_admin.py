from app import create_app
from app.services import facade

def create_admin_user():
    """Create the first admin user"""
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        admin_email = "admin@hbnb.com"
        existing_admin = facade.get_user_by_email(admin_email)
        
        if existing_admin:
            print(f"Admin user already exists: {admin_email}")
            return existing_admin
        
        # Create admin user
        admin_data = {
            'first_name': 'Admin',
            'last_name': 'User',
            'email': admin_email,
            'password': 'admin123',
            'is_admin': True
        }
        
        try:
            admin_user = facade.create_user(admin_data)
            print(f"Admin user created successfully!")
            print(f"Email: {admin_user.email}")
            print(f"ID: {admin_user.id}")
            print(f"Password: admin123")
            return admin_user
        except Exception as e:
            print(f"Error creating admin user: {e}")
            return None

if __name__ == "__main__":
    create_admin_user()