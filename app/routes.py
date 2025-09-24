# app/routes.py
from flask import Blueprint, request, jsonify, current_app
from . import db
from .models import Patient, ClinicalStudy, Production
from datetime import date

bp = Blueprint("main", __name__)

# ---------------------------
# Helpers
# ---------------------------
def parse_date_iso(value):
    """Tenta converter uma string ISO (YYYY-MM-DD) para date."""
    if not value:
        return None
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(value)
    except Exception:
        return None

def bad_request(msg):
    return jsonify({"error": msg}), 400

# ---------------------------
# HEALTH
# ---------------------------
@bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

# ---------------------------
# PATIENTS - CRUD
# ---------------------------
@bp.route("/patients", methods=["GET"])
def get_patients():
    patients = Patient.query.all()
    return jsonify([p.to_dict() for p in patients]), 200


@bp.route("/patients/<int:patient_id>", methods=["GET"])
def get_patient(patient_id):
    p = Patient.query.get_or_404(patient_id)
    return jsonify(p.to_dict()), 200


@bp.route("/patients", methods=["POST"])
def create_patient():
    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return bad_request("Field 'name' is required.")
    birth_date = parse_date_iso(data.get("birth_date"))
    if data.get("birth_date") and not birth_date:
        return bad_request("Field 'birth_date' must be YYYY-MM-DD or null.")
    p = Patient(name=name, birth_date=birth_date)
    db.session.add(p)
    db.session.commit()
    return jsonify({"message": "Patient created", "id": p.id}), 201


@bp.route("/patients/<int:patient_id>", methods=["PUT", "PATCH"])
def update_patient(patient_id):
    p = Patient.query.get_or_404(patient_id)
    data = request.get_json() or {}
    if "name" in data:
        p.name = data["name"]
    if "birth_date" in data:
        bd = parse_date_iso(data.get("birth_date"))
        if data.get("birth_date") and not bd:
            return bad_request("Field 'birth_date' must be YYYY-MM-DD or null.")
        p.birth_date = bd
    db.session.commit()
    return jsonify({"message": "Patient updated", "patient": p.to_dict()}), 200


@bp.route("/patients/<int:patient_id>", methods=["DELETE"])
def delete_patient(patient_id):
    p = Patient.query.get_or_404(patient_id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "Patient deleted"}), 200

# ---------------------------
# STUDIES - CRUD
# ---------------------------
@bp.route("/studies", methods=["GET"])
def get_studies():
    studies = ClinicalStudy.query.all()
    return jsonify([s.to_dict() for s in studies]), 200


@bp.route("/studies/<int:study_id>", methods=["GET"])
def get_study(study_id):
    s = ClinicalStudy.query.get_or_404(study_id)
    return jsonify(s.to_dict()), 200


@bp.route("/studies", methods=["POST"])
def create_study():
    data = request.get_json() or {}
    title = data.get("title")
    if not title:
        return bad_request("Field 'title' is required.")
    status = data.get("status", "planning")
    s = ClinicalStudy(title=title, status=status)
    db.session.add(s)
    db.session.commit()
    return jsonify({"message": "Study created", "id": s.id}), 201


@bp.route("/studies/<int:study_id>", methods=["PUT", "PATCH"])
def update_study(study_id):
    s = ClinicalStudy.query.get_or_404(study_id)
    data = request.get_json() or {}
    if "title" in data:
        s.title = data["title"]
    if "status" in data:
        s.status = data["status"]
    # Optionally manage patient associations
    if "patient_ids" in data:
        if not isinstance(data["patient_ids"], list):
            return bad_request("Field 'patient_ids' must be a list of integers.")
        # replace associations
        from .models import Patient
        patients = Patient.query.filter(Patient.id.in_(data["patient_ids"])).all()
        s.patients = patients
    db.session.commit()
    return jsonify({"message": "Study updated", "study": s.to_dict()}), 200


@bp.route("/studies/<int:study_id>", methods=["DELETE"])
def delete_study(study_id):
    s = ClinicalStudy.query.get_or_404(study_id)
    db.session.delete(s)
    db.session.commit()
    return jsonify({"message": "Study deleted"}), 200

# ---------------------------
# PRODUCTION - CRUD
# ---------------------------
@bp.route("/productions", methods=["GET"])
def get_productions():
    prods = Production.query.all()
    return jsonify([p.to_dict() for p in prods]), 200


@bp.route("/productions/<int:prod_id>", methods=["GET"])
def get_production(prod_id):
    p = Production.query.get_or_404(prod_id)
    return jsonify(p.to_dict()), 200


@bp.route("/productions", methods=["POST"])
def create_production():
    data = request.get_json() or {}
    batch_number = data.get("batch_number")
    product_name = data.get("product_name")
    quantity = data.get("quantity")
    if not batch_number or not product_name or quantity is None:
        return bad_request("Fields 'batch_number', 'product_name' and 'quantity' are required.")
    try:
        quantity = int(quantity)
    except ValueError:
        return bad_request("'quantity' must be an integer.")
    # check uniqueness
    if Production.query.filter_by(batch_number=batch_number).first():
        return bad_request("batch_number already exists.")
    p = Production(batch_number=batch_number, product_name=product_name, quantity=quantity, status=data.get("status", "in_progress"))
    db.session.add(p)
