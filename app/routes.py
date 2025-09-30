# app/routes.py
# Rotas mínimas (REST-like) para CRUD básico (create + list + detail).
# MODIF: criado/atualizado com endpoints para Users, ClinicalStudy e Product
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from . import db
from .models import User, ClinicalStudy, Product
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

main_bp = Blueprint("main", __name__)

# Página inicial simples
@main_bp.route("/")
def index():
    return render_template("index.html")  # MODIF: novo template

# --------------------------
# Usuários
# --------------------------
@main_bp.route("/api/users", methods=["POST"])
def create_user():
    """Cria usuário. Espera JSON com name, email, password."""
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not (name and email and password):
        return jsonify({"error": "name, email and password are required"}), 400

    # Verificar se email já existe
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email already registered"}), 400

    password_hash = generate_password_hash(password)  # MODIF: usamos werkzeug para hash
    user = User(name=name, email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@main_bp.route("/api/users", methods=["GET"])
def list_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@main_bp.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

# --------------------------
# Estudos clínicos
# --------------------------
@main_bp.route("/api/studies", methods=["POST"])
def create_study():
    """Cria estudo clínico. JSON: title, description, start_date (YYYY-MM-DD), end_date"""
    data = request.get_json() or {}
    title = data.get("title")
    if not title:
        return jsonify({"error": "title is required"}), 400

    # Parse dates de forma simples
    def parse_date(s):
        if not s:
            return None
        try:
            return datetime.fromisoformat(s).date()
        except Exception:
            return None

    start_date = parse_date(data.get("start_date"))
    end_date = parse_date(data.get("end_date"))

    study = ClinicalStudy(title=title, description=data.get("description"), start_date=start_date, end_date=end_date)
    db.session.add(study)
    db.session.commit()
    return jsonify(study.to_dict()), 201

@main_bp.route("/api/studies", methods=["GET"])
def list_studies():
    studies = ClinicalStudy.query.order_by(ClinicalStudy.created_at.desc()).all()
    return jsonify([s.to_dict() for s in studies])

@main_bp.route("/api/studies/<int:study_id>", methods=["GET"])
def get_study(study_id):
    s = ClinicalStudy.query.get_or_404(study_id)
    return jsonify(s.to_dict())

# --------------------------
# Produtos farmacêuticos
# --------------------------
@main_bp.route("/api/products", methods=["POST"])
def create_product():
    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "name is required"}), 400

    expiry_date = None
    if data.get("expiry_date"):
        try:
            expiry_date = datetime.fromisoformat(data.get("expiry_date")).date()
        except Exception:
            return jsonify({"error": "expiry_date must be ISO date YYYY-MM-DD"}), 400

    p = Product(name=name, batch=data.get("batch"), expiry_date=expiry_date)
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201

@main_bp.route("/api/products", methods=["GET"])
def list_products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return jsonify([p.to_dict() for p in products])

@main_bp.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    p = Product.query.get_or_404(product_id)
    return jsonify(p.to_dict())

# --------------------------
# Rotas simples com templates (interface mínima)
# --------------------------
@main_bp.route("/studies")
def studies_page():
    studies = ClinicalStudy.query.order_by(ClinicalStudy.created_at.desc()).all()
    return render_template("studies.html", studies=studies)

@main_bp.route("/products")
def products_page():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template("products.html", products=products)

@main_bp.route("/users")
def users_page():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("users.html", users=users)
