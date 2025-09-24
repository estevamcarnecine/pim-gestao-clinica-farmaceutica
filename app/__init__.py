# app/__init__.py
# Factory da aplicação e inicialização das extensões.
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()  # carrega .env se presente

db = SQLAlchemy()
migrate = Migrate()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(os.getcwd(), 'instance', 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'trocar_esta_chave_para_prod')
    JSON_SORT_KEYS = False  # manter ordem para legibilidade

def create_app(config_object=None):
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__, instance_relative_config=True)

    # Carrega config: se config_object for passado, usa-o; senão usa Config padrão
    if config_object:
        app.config.from_object(config_object)
    else:
        app.config.from_object(Config)

    # garante que a pasta instance exista (onde fica o sqlite por padrão)
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except Exception:
        pass

    db.init_app(app)
    migrate.init_app(app, db)

    # importa modelos para que o Flask-Migrate os detecte
    from . import models  # noqa: F401

    # registra blueprints
    from .routes import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/api')

    # health-check root (opcional)
    @app.route('/')
    def index():
        return {'status': 'ok', 'service': 'pim-gestao-clinica-farmaceutica'}, 200

    return app
