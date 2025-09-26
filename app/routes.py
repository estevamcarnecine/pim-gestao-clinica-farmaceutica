from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Patient

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/')
def index():
    return redirect(url_for('patients.list_patients'))

@patients_bp.route('/patients')
def list_patients():
    patients = Patient.query.all()
    return render_template('patients.html', patients=patients)

@patients_bp.route('/patients/create', methods=['GET', 'POST'])
def create_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        condition = request.form['condition']
        if not name or not age:
            flash("Name and age are required!", "error")
            return redirect(url_for('patients.create_patient'))

        new_patient = Patient(name=name, age=age, condition=condition)
        db.session.add(new_patient)
        db.session.commit()
        flash("Patient created successfully!", "success")
        return redirect(url_for('patients.list_patients'))

    return render_template('create_patient.html')

# -------- NEW ROUTES --------

@patients_bp.route('/patients/update/<int:id>', methods=['GET', 'POST'])
def update_patient(id):
    patient = Patient.query.get_or_404(id)

    if request.method == 'POST':
        patient.name = request.form['name']
        patient.age = request.form['age']
        patient.condition = request.form['condition']

        db.session.commit()
        flash("Patient updated successfully!", "success")
        return redirect(url_for('patients.list_patients'))

    return render_template('update_patient.html', patient=patient)

@patients_bp.route('/patients/delete/<int:id>', methods=['POST'])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    flash("Patient deleted successfully!", "success")
    return redirect(url_for('patients.list_patients'))
