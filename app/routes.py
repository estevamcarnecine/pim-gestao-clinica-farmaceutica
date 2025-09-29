from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Patient, ClinicalStudy
from datetime import datetime

patients_bp = Blueprint('patients_bp', __name__) # blueprint criado aqui

@patients_bp.route("/")
def index():
    return "Hello Patients" #teste inicial

main = Blueprint("main", __name__)

# Home route
@main.route("/")
def index():
    return redirect(url_for("main.list_patients"))

# List all patients
@main.route("/patients")
def list_patients():
    patients = Patient.query.all()
    return render_template("patients.html", patients=patients)

# Create a new patient
@main.route("/patients/new", methods=["GET", "POST"])
def new_patient():
    if request.method == "POST":
        name = request.form.get("name")
        birth_date = request.form.get("birth_date")

        if birth_date:
            birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        else:
            birth_date = None

        new_patient = Patient(name=name, birth_date=birth_date)
        db.session.add(new_patient)
        db.session.commit()
        return redirect(url_for("main.confirmation"))

    return render_template("edit_patient.html", patient=None)

# Confirmation page after adding a patient
@main.route("/confirmation")
def confirmation():
    return render_template("confirmation.html")

# Edit an existing patient  <-- NEW
@main.route("/patients/edit/<int:patient_id>", methods=["GET", "POST"])
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if request.method == "POST":
        patient.name = request.form.get("name")
        birth_date = request.form.get("birth_date")

        if birth_date:
            patient.birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        else:
            patient.birth_date = None

        db.session.commit()
        return redirect(url_for("main.list_patients"))

    return render_template("edit_patient.html", patient=patient)

# Delete a patient  <-- NEW
@main.route("/patients/delete/<int:patient_id>", methods=["POST"])
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for("main.list_patients"))
