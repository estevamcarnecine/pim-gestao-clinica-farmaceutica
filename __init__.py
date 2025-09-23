from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migreate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_object='app.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app