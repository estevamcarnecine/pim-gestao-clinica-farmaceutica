import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY', 'trocar_esta_chave_para_prod')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False