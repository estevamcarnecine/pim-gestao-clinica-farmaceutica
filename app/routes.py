from flask import Blueprint, render_template, redirect, url_for, request
from app.models import Patient, db

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    patients = Patient.query.all()
    return render_template("patients.html", patients=patients)

@bp.route("/add_patient", methods=["POST"])
def add_patient():
    name = request.form.get("name")
    age = request.form.get("age")
    diagnosis = request.form.get("diagnosis")

    new_patient = Patient(name=name, age=age, diagnosis=diagnosis)
    db.session.add(new_patient)
    db.session.commit()

    return redirect(url_for("main.index"))
