from flask import jsonify, request, render_template
from app import app, db
from app.models import Patient

# Home page
@app.route("/")
def index():
    return render_template("base.html")

# Get all patients (JSON API)
@app.route("/api/patients", methods=["GET"])
def get_patients():
    patients = Patient.query.all()
    return jsonify([{"id": p.id, "name": p.name} for p in patients])

# Add a new patient
@app.route("/api/patients", methods=["POST"])
def add_patient():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Invalid data"}), 400

    patient = Patient(name=data["name"])
    db.session.add(patient)
    db.session.commit()
    return jsonify({"id": patient.id, "name": patient.name}), 201
