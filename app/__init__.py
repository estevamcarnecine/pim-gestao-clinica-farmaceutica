import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

db = SQLAlchemy()

def create_app():


    load_dotenv()  # carrega .env se existir
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Configurações mínimas
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')  # MODIF: adicionado
    # Usa SQLite local para facilidade (arquivo db.sqlite na raiz)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///../db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Importa modelos e rotas aqui para evitar import circular
    with app.app_context():
        from . import models  # MODIF: garantir que modelos sejam carregados
        db.create_all()  # Cria tabelas automaticamente no primeiro run (simplicidade para MVP). MODIF: adicionado

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
