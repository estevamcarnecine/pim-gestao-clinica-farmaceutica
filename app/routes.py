from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Patient

# Define Blueprint
bp = Blueprint("main", __name__)

# Home route
@bp.route("/")
def index():
    return redirect(url_for("main.patients"))

# List patients
@bp.route("/patients")
def patients():
    patients_list = Patient.query.all()
    return render_template("patients.html", patients=patients_list)

# Add new patient
@bp.route("/patients/new", methods=["GET", "POST"])
def new_patient():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        diagnosis = request.form.get("diagnosis")

        patient = Patient(name=name, age=age, diagnosis=diagnosis)
        db.session.add(patient)
        db.session.commit()

        return redirect(url_for("main.confirmation"))

    return render_template("new_patient.html")

# Confirmation page after creating patient
@bp.route("/patients/confirmation")
def confirmation():
    return render_template("confirmation.html")

# Edit patient  ← (ADDED)
@bp.route("/patients/edit/<int:id>", methods=["GET", "POST"])
def edit_patient(id):
    patient = Patient.query.get_or_404(id)

    if request.method == "POST":
        patient.name = request.form.get("name")
        patient.age = request.form.get("age")
        patient.diagnosis = request.form.get("diagnosis")

        db.session.commit()
        return redirect(url_for("main.patients"))

    return render_template("edit_patient.html", patient=patient)

# Delete patient  ← (ADDED)
@bp.route("/patients/delete/<int:id>", methods=["POST"])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for("main.patients"))
