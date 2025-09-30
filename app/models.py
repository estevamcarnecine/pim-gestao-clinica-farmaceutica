# app/models.py
# Modelos SQLAlchemy para o MVP: User, ClinicalStudy, Product.
# MODIF: novo/consolidado

from . import db
from datetime import datetime

# Usuários simples com senha criptografada (bcrypt)
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)  # MODIF: novo campo
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)  # armazenar hash
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        # Retorna dicionário para JSON (nunca retornar password_hash).
        return {"id": self.id, "name": self.name, "email": self.email, "created_at": self.created_at.isoformat()}

class ClinicalStudy(db.Model):
    __tablename__ = "clinical_studies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "created_at": self.created_at.isoformat()
        }

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    batch = db.Column(db.String(100))
    expiry_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "batch": self.batch,
            "expiry_date": self.expiry_date.isoformat() if self.expiry_date else None,
            "created_at": self.created_at.isoformat()
        }
