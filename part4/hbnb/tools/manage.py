#!/usr/bin/env python3
"""Management helper script for HBnB.
Allows renaming a host user and adding a new place without resetting the DB.

Usage examples:

    python3 part4/hbnb/tools/manage.py rename-host --email host@example.com --first Zed --last Shadow
    python3 part4/hbnb/tools/manage.py add-place --host-email host@example.com --name "Jungle Retreat" --description "Hidden spot" --price 140 --amenities WiFi Kitchen
    python3 part4/hbnb/tools/manage.py add-host --email rengar@example.com --first Rengar --last Hunter --password password
    python3 part4/hbnb/tools/manage.py list-places
    python3 part4/hbnb/tools/manage.py reassign-host --place-id <uuid> --host-email rengar@example.com
    python3 part4/hbnb/tools/manage.py assign-image --place-id <uuid> --image "Anor Londo.avif" --rename "Anor Londo"

"""
import sys
import os
import argparse

# Ensure part4/hbnb path is on sys.path so 'app' package resolves when running from repo root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app
from app.extensions import db
from app.models import User, Place, Amenity
from sqlalchemy import inspect, text

app = create_app()


def rename_host(email: str, first: str, last: str):
    with app.app_context():
        user = User.query.filter_by(email=email.lower()).first()
        if not user:
            print(f"[ERROR] User with email {email} not found")
            return 1
        old = f"{user.first_name} {user.last_name}".strip()
        user.first_name = first
        user.last_name = last
        db.session.commit()
        print(f"[OK] Renamed host '{old}' -> '{first} {last}' (id={user.id})")
        return 0


def add_place(host_email: str, name: str, description: str, price: float, amenity_names):
    with app.app_context():
        host = User.query.filter_by(email=host_email.lower()).first()
        if not host:
            print(f"[ERROR] Host with email {host_email} not found")
            return 1
        if price < 0:
            print("[ERROR] Price must be >= 0")
            return 1
        amenities = []
        if amenity_names:
            for an in amenity_names:
                am = Amenity.query.filter_by(name=an).first()
                if not am:
                    print(f"[WARN] Amenity '{an}' not found – skipping")
                    continue
                amenities.append(am)
        place = Place(name=name, description=description, price_per_night=price, host_id=host.id)
        place.amenities.extend(amenities)
        db.session.add(place)
        db.session.commit()
        print(f"[OK] Added place '{name}' (id={place.id}) for host {host.first_name} {host.last_name}")
        return 0


def add_host(email: str, first: str, last: str, password: str):
    """Create a new host user if email not already used."""
    with app.app_context():
        existing = User.query.filter_by(email=email.lower()).first()
        if existing:
            print(f"[ERROR] User with email {email} already exists (id={existing.id})")
            return 1
        u = User(first_name=first, last_name=last, email=email.lower())
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        print(f"[OK] Created host '{first} {last}' (email={email}, id={u.id})")
        return 0


def list_places():
    """List all places with their current host name/email."""
    with app.app_context():
        _ensure_image_column()
        places = Place.query.all()
        if not places:
            print("[INFO] No places found.")
            return 0
        print(f"[INFO] {len(places)} places:")
        for p in places:
            host = p.host
            host_name = f"{host.first_name} {host.last_name}".strip() if host else "<no host>"
            img = p.image_filename or '<none>'
            print(f" - id={p.id} name='{p.name}' image='{img}' host='{host_name}' email={host.email if host else 'n/a'}")
        return 0


def reassign_host(place_id: str, host_email: str):
    """Change the host of a given place."""
    with app.app_context():
        place = Place.query.filter_by(id=place_id).first()
        if not place:
            print(f"[ERROR] Place with id {place_id} not found")
            return 1
        new_host = User.query.filter_by(email=host_email.lower()).first()
        if not new_host:
            print(f"[ERROR] Host with email {host_email} not found")
            return 1
        old_host = place.host
        place.host_id = new_host.id
        db.session.commit()
        print(f"[OK] Reassigned place '{place.name}' (id={place.id}) host: '{old_host.first_name} {old_host.last_name}' -> '{new_host.first_name} {new_host.last_name}'")
        return 0


def assign_image(place_id: str, image: str, rename: str = None):
    """Assign an image file (already placed in static/img) to a place and optionally rename the place."""
    with app.app_context():
        _ensure_image_column()
        place = Place.query.filter_by(id=place_id).first()
        if not place:
            print(f"[ERROR] Place with id {place_id} not found")
            return 1
        # Basic validation: disallow path traversal
        if '/' in image or '\\' in image:
            print('[ERROR] Image filename must not contain path separators')
            return 1
        place.image_filename = image
        old_name = place.name
        if rename:
            place.name = rename
        db.session.commit()
        print(f"[OK] Assigned image '{image}' to place id={place.id} name='{place.name}' (was '{old_name}')")
        return 0


def promote_user(email: str):
    """Set is_admin=True for the user with given email."""
    with app.app_context():
        user = User.query.filter_by(email=email.lower()).first()
        if not user:
            print(f"[ERROR] User with email {email} not found")
            return 1
        if user.is_admin:
            print(f"[INFO] User {email} is already admin")
            return 0
        user.is_admin = True
        db.session.commit()
        print(f"[OK] Promoted user {email} to admin (id={user.id})")
        return 0


def demote_user(email: str):
    """Remove admin privileges from the user (is_admin=False)."""
    with app.app_context():
        user = User.query.filter_by(email=email.lower()).first()
        if not user:
            print(f"[ERROR] User with email {email} not found")
            return 1
        if not user.is_admin:
            print(f"[INFO] User {email} is not admin already")
            return 0
        user.is_admin = False
        db.session.commit()
        print(f"[OK] Demoted user {email} from admin (id={user.id})")
        return 0


def list_users():
    """List all users with admin flag."""
    with app.app_context():
        users = User.query.all()
        if not users:
            print('[INFO] No users found.')
            return 0
        print(f"[INFO] {len(users)} users:\nemail | name | is_admin | id")
        for u in users:
            print(f" - {u.email} | {u.first_name} {u.last_name} | {'admin' if u.is_admin else 'user'} | {u.id}")
        return 0


def set_place_description(place_id: str, description: str):
    """Update the description text of a place (dark fantasy theming, etc.)."""
    with app.app_context():
        place = Place.query.filter_by(id=place_id).first()
        if not place:
            print(f"[ERROR] Place with id {place_id} not found")
            return 1
        place.description = description
        db.session.commit()
        print(f"[OK] Updated description for place '{place.name}' (id={place.id})")
        return 0


def build_parser():
    p = argparse.ArgumentParser(description="HBnB management commands")
    sub = p.add_subparsers(dest="command", required=True)

    r = sub.add_parser("rename-host", help="Rename a host user by email")
    r.add_argument("--email", required=True, help="Email of existing user")
    r.add_argument("--first", required=True, help="New first name")
    r.add_argument("--last", required=True, help="New last name")

    a = sub.add_parser("add-place", help="Add a new place for a host")
    a.add_argument("--host-email", required=True, help="Email of host user")
    a.add_argument("--name", required=True, help="Place name")
    a.add_argument("--description", default="", help="Place description")
    a.add_argument("--price", type=float, required=True, help="Price per night")
    a.add_argument("--amenities", nargs='*', help="Amenity names to attach (optional)")

    h = sub.add_parser("add-host", help="Create a new host user")
    h.add_argument("--email", required=True, help="Email for new host user")
    h.add_argument("--first", required=True, help="First name")
    h.add_argument("--last", required=True, help="Last name")
    h.add_argument("--password", default="password", help="Password (default: password)")

    lp = sub.add_parser("list-places", help="List all places with host info")

    rh = sub.add_parser("reassign-host", help="Change the host for a place")
    rh.add_argument("--place-id", required=True, help="Place id (UUID)")
    rh.add_argument("--host-email", required=True, help="Email of target host")

    ai = sub.add_parser("assign-image", help="Assign an image to a place")
    ai.add_argument("--place-id", required=True, help="Place id (UUID)")
    ai.add_argument("--image", required=True, help="Image filename (must exist in static/img)")
    ai.add_argument("--rename", help="Optional new place name to match image")

    sd = sub.add_parser("set-description", help="Update a place description")
    sd.add_argument("--place-id", required=True, help="Place id (UUID)")
    sd.add_argument("--description", required=True, help="New description text")

    pu = sub.add_parser("promote-user", help="Grant admin rights to user")
    pu.add_argument("--email", required=True, help="User email")

    du = sub.add_parser("demote-user", help="Remove admin rights from user")
    du.add_argument("--email", required=True, help="User email")

    lu = sub.add_parser("list-users", help="List all users with admin flag")
    return p

def _ensure_image_column():
    """Runtime migration for image_filename if missing (usable when run.py not invoked)."""
    inspector = inspect(db.engine)
    cols = [c['name'] for c in inspector.get_columns('places')]
    if 'image_filename' not in cols:
        try:
            db.session.execute(text('ALTER TABLE places ADD COLUMN image_filename VARCHAR(255)'))
            db.session.commit()
            print('[INFO] Added image_filename column to places table')
        except Exception as e:
            print(f'[WARN] Could not add image_filename column: {e}')


def main(argv):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == 'rename-host':
        return rename_host(args.email, args.first, args.last)
    if args.command == 'add-place':
        return add_place(args.host_email, args.name, args.description, args.price, args.amenities)
    if args.command == 'add-host':
        return add_host(args.email, args.first, args.last, args.password)
    if args.command == 'list-places':
        return list_places()
    if args.command == 'reassign-host':
        return reassign_host(args.place_id, args.host_email)
    if args.command == 'assign-image':
        return assign_image(args.place_id, args.image, args.rename)
    if args.command == 'set-description':
        return set_place_description(args.place_id, args.description)
    if args.command == 'promote-user':
        return promote_user(args.email)
    if args.command == 'demote-user':
        return demote_user(args.email)
    if args.command == 'list-users':
        return list_users()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
