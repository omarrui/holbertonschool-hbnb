import os
import sys
from app import create_app
from app.extensions import db, bcrypt
from app import models  # ensure all models imported
from app.models import User, Place, Amenity, Review
from sqlalchemy import inspect, text

app = create_app()

def seed_demo_data():
    """Populate demo data if database empty."""
    # If places already exist, skip seeding to avoid duplicates
    if Place.query.count() > 0:
        return
    # Create multiple host users with requested names
    hosts = []
    for first,last,email in [
        ('Zed','Shadow','zed@example.com'),
        ('Rengar','Hunter','rengar@example.com'),
        ('Darius','Hand','darius@example.com')
    ]:
        u = User(first_name=first, last_name=last, email=email)
        u.set_password('password')
        db.session.add(u)
        hosts.append(u)

    wifi = Amenity(name='WiFi'); kitchen = Amenity(name='Kitchen'); parking = Amenity(name='Parking')
    db.session.add_all([wifi, kitchen, parking])
    db.session.flush()

    # Assign places to different hosts
    p1 = Place(name='Cozy Apartment', description='A cozy downtown apartment near cafes.', price_per_night=90, host_id=hosts[0].id)
    p1.amenities.extend([wifi, kitchen])
    p2 = Place(name='Beach House', description='Sunny house overlooking the sea.', price_per_night=150, host_id=hosts[1].id)
    p2.amenities.extend([wifi, parking])
    p3 = Place(name='City Loft', description='Modern loft in business district.', price_per_night=120, host_id=hosts[2].id)
    p3.amenities.extend([wifi])
    db.session.add_all([p1, p2, p3])
    db.session.flush()

    # Seed one review per place by its host
    reviews = [
        Review(place_id=p1.id, user_id=hosts[0].id, rating=5, comment='Shadow approves this stay.'),
        Review(place_id=p2.id, user_id=hosts[1].id, rating=4, comment='Great for hunting sunsets.'),
        Review(place_id=p3.id, user_id=hosts[2].id, rating=5, comment='Strong location, solid comfort.')
    ]
    db.session.add_all(reviews)
    db.session.commit()

def ensure_place_image_column():
    """Add image_filename column to places table if missing (simple runtime migration)."""
    inspector = inspect(db.engine)
    cols = [c['name'] for c in inspector.get_columns('places')]
    if 'image_filename' not in cols:
        try:
            db.session.execute(text('ALTER TABLE places ADD COLUMN image_filename VARCHAR(255)'))
            db.session.commit()
            print('[INFO] Added image_filename column to places table')
        except Exception as e:
            print(f'[WARN] Failed to add image_filename column: {e}')

def _resolve_port():
    # Priority: --port=XXXX arg > PORT env > default 5000
    for arg in sys.argv[1:]:
        if arg.startswith('--port='):
            try:
                return int(arg.split('=', 1)[1])
            except ValueError:
                pass
    env_port = os.environ.get('PORT')
    if env_port:
        try:
            return int(env_port)
        except ValueError:
            pass
    return 5000

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        ensure_place_image_column()
        seed_demo_data()

    host = os.environ.get('HOST', '127.0.0.1')
    port = _resolve_port()
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'

    try:
        app.run(host=host, port=port, debug=debug)
    except OSError as e:
        if 'Address already in use' in str(e):
            print(f"Port {port} already in use. Try: python3 part4/hbnb/run.py --port=5001")
        raise
