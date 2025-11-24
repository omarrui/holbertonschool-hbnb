from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from flask_restx import Api
from app.extensions import db, bcrypt, jwt
from flask_jwt_extended import decode_token
from app.models import User, Place, Review, Amenity
from config import config

from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns

def create_app(config_name: str = 'development'):
    app = Flask(__name__)
    cfg = config.get(config_name, config['default'])
    app.config.from_object(cfg)

    # init extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Attach before_request to read JWT cookie for user session bridging
    @app.before_request
    def load_user_from_token():
        if 'user_id' in session:
            return
        token = request.cookies.get('token')
        if not token:
            return
        try:
            decoded = decode_token(token)
            identity = decoded.get('sub')  # JWT identity
            if identity:
                session['user_id'] = identity
        except Exception:
            # Invalid token: ignore silently (could optionally clear cookie)
            pass

    # Configure API docs away from root to free '/' for HTML site
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/docs',          # Swagger UI now at /api/docs
        prefix='/api/v1'          # All endpoints under /api/v1
    )

    # Namespace paths now relative to prefix
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(users_ns, path='/users')
    api.add_namespace(places_ns, path='/places')
    api.add_namespace(amenities_ns, path='/amenities')
    api.add_namespace(reviews_ns, path='/reviews')

    # --- Web (HTML) Routes ---
    @app.route('/')
    def index():
        places = Place.query.all()
        return render_template('index.html', places=places)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session['user_id'] = user.id
                flash('Login successful', 'success')
                return redirect(url_for('index'))
            flash('Invalid credentials', 'error')
        return render_template('login.html')

    @app.route('/register', methods=['GET'])
    def register():
        return render_template('register.html')

    @app.route('/place/<string:place_id>')
    def place_details(place_id: str):
        place = Place.query.get_or_404(place_id)
        reviews = Review.query.filter_by(place_id=place.id).all()
        return render_template('place.html', place=place, reviews=reviews)

    # Alias plural route for compatibility (old links or cached JS)
    @app.route('/places/<string:place_id>')
    def place_details_alias(place_id: str):
        return redirect(url_for('place_details', place_id=place_id))

    @app.route('/place/<string:place_id>/review/add', methods=['GET', 'POST'])
    def add_review(place_id: str):
        place = Place.query.get_or_404(place_id)
        if request.method == 'POST':
            if 'user_id' not in session:
                flash('Login required to add a review', 'error')
                return redirect(url_for('login'))
            rating = request.form.get('rating', type=int)
            comment = request.form.get('comment', '').strip()
            if not rating or rating < 1 or rating > 5:
                flash('Rating must be between 1 and 5', 'error')
                return redirect(url_for('add_review', place_id=place.id))
            if not comment:
                flash('Comment required', 'error')
                return redirect(url_for('add_review', place_id=place.id))
            review = Review(place_id=place.id, user_id=session['user_id'], rating=rating, comment=comment)
            db.session.add(review)
            db.session.commit()
            flash('Review added', 'success')
            return redirect(url_for('place_details', place_id=place.id))
        # GET: Render template regardless of auth; front-end JS redirects unauthenticated users to index
        return render_template('add_review.html', place=place)

    @app.route('/place/new', methods=['GET'])
    def new_place():
        if 'user_id' not in session:
            flash('Login required to create a place', 'error')
            return redirect(url_for('login'))
        return render_template('create_place.html')

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        flash('Logged out', 'success')
        return redirect(url_for('index'))

    return app
