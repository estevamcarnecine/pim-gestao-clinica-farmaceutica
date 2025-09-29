from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

def create_app():
    """
    Factory function to create and configure the Flask app
    """
    app = Flask(__name__)

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # SQLite database file
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the app
    db.init_app(app)

    # Import Blueprints
    from app.routes import patients_bp  # <-- Blueprint for patient routes

    # Register Blueprints
    app.register_blueprint(patients_bp)  # <-- Register the blueprint with the app

    # You can add more Blueprints here in the future (e.g., auth, admin)

    return app
