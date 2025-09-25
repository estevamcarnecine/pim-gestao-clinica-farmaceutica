from flask import Blueprint, request, jsonify
from . import db
from .models import Patient, ClinicalStudy, Production

bp = Blueprint("main", __name__)

# ------------------------
# Patients
# ------------------------
@bp.route("/api/patients", methods=["GET"])
def get_patients():
    patients = Patient.query.all()
    return jsonify([{"id": p.id, "name": p.name} for p in patients])

@bp.route("/api/patients", methods=["POST"])
def create_patient():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Campo 'name' é obrigatório"}), 400

    patient = Patient(name=data["name"])
    db.session.add(patient)
    db.session.commit()
    return jsonify({"id": patient.id, "name": patient.name}), 201

@bp.route("/api/patients/<int:id>", methods=["PUT"])
def update_patient(id):
    patient = Patient.query.get_or_404(id)
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Campo 'name' é obrigatório"}), 400

    patient.name = data["name"]
    db.session.commit()
    return jsonify({"id": patient.id, "name": patient.name})

@bp.route("/api/patients/<int:id>", methods=["DELETE"])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({"message": f"Paciente {patient.id} removido com sucesso"})


# ------------------------
# Clinical Studies
# ------------------------
@bp.route("/api/studies", methods=["GET"])
def get_studies():
    studies = ClinicalStudy.query.all()
    return jsonify([{"id": s.id, "title": s.title, "status": s.status} for s in studies])

@bp.route("/api/studies", methods=["POST"])
def create_study():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Campo 'title' é obrigatório"}), 400

    study = ClinicalStudy(title=data["title"])
    db.session.add(study)
    db.session.commit()
    return jsonify({"id": study.id, "title": study.title, "status": study.status}), 201

@bp.route("/api/studies/<int:id>", methods=["PUT"])
def update_study(id):
    study = ClinicalStudy.query.get_or_404(id)
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Campo 'title' é obrigatório"}), 400

    study.title = data["title"]
    if "status" in data:
        study.status = data["status"]

    db.session.commit()
    return jsonify({"id": study.id, "title": study.title, "status": study.status})

@bp.route("/api/studies/<int:id>", methods=["DELETE"])
def delete_study(id):
    study = ClinicalStudy.query.get_or_404(id)
    db.session.delete(study)
    db.session.commit()
    return jsonify({"message": f"Estudo clínico {study.id} removido com sucesso"})


# ------------------------
# Productions
# ------------------------
@bp.route("/api/productions", methods=["GET"])
def get_productions():
    productions = Production.query.all()
    return jsonify([{"id": p.id, "batch_number": p.batch_number} for p in productions])

@bp.route("/api/productions", methods=["POST"])
def create_production():
    data = request.get_json()
    if not data or "batch_number" not in data:
        return jsonify({"error": "Campo 'batch_number' é obrigatório"}), 400

    production = Production(batch_number=data["batch_number"])
    db.session.add(production)
    db.session.commit()
    return jsonify({"id": production.id, "batch_number": production.batch_number}), 201

@bp.route("/api/productions/<int:id>", methods=["PUT"])
def update_production(id):
    production = Production.query.get_or_404(id)
    data = request.get_json()

    if not data or "batch_number" not in data:
        return jsonify({"error": "Campo 'batch_number' é obrigatório"}), 400

    production.batch_number = data["batch_number"]
    db.session.commit()
    return jsonify({"id": production.id, "batch_number": production.batch_number})

@bp.route("/api/productions/<int:id>", methods=["DELETE"])
def delete_production(id):
    production = Production.query.get_or_404(id)
    db.session.delete(production)
    db.session.commit()
    return jsonify({"message": f"Lote de produção {production.id} removido com sucesso"})
