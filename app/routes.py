from flask import Blueprint, request, jsonify
from . import db
from .models import Patient, ClinicalStudy, Production

# Usamos Blueprint para organizar as rotas
bp = Blueprint("main", __name__)

# ---------------------------
# PACIENTES
# ---------------------------
@bp.route("/patients", methods=["GET"])
def get_patients():
    patients = Patient.query.all()
    return jsonify([{"id": p.id, "name": p.name, "birth_date": str(p.birth_date)} for p in patients])


@bp.route("/patients", methods=["POST"])
def create_patient():
    data = request.get_json()
    new_patient = Patient(name=data["name"], birth_date=data.get("birth_date"))
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({"message": "Patient created", "id": new_patient.id}), 201


# ---------------------------
# ESTUDOS CLÍNICOS
# ---------------------------
@bp.route("/studies", methods=["GET"])
def get_studies():
    studies = ClinicalStudy.query.all()
    return jsonify([{"id": s.id, "title": s.title, "status": s.status} for s in studies])


@bp.route("/studies", methods=["POST"])
def create_study():
    data = request.get_json()
    new_study = ClinicalStudy(title=data["title"], status=data.get("status", "planning"))
    db.session.add(new_study)
    db.session.commit()
    return jsonify({"message": "Study created", "id": new_study.id}), 201


# ---------------------------
# PRODUÇÃO FARMACÊUTICA
# ---------------------------
@bp.route("/production", methods=["GET"])
def get_production():
    productions = Production.query.all()
    return jsonify([
        {"id": p.id, "batch_number": p.batch_number, "product_name": p.product_name, "quantity": p.quantity, "status": p.status}
        for p in productions
    ])


@bp.route("/production", methods=["POST"])
def create_production():
    data = request.get_json()
    new_prod = Production(
        batch_number=data["batch_number"],
        product_name=data["product_name"],
        quantity=data["quantity"],
        status=data.get("status", "in_progress")
    )
    db.session.add(new_prod)
    db.session.commit()
    return jsonify({"message": "Production created", "id": new_prod.id}), 201
