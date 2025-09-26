from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Patient

patients_bp = Blueprint('patients', __name__)

# ---------------- Home / Index ----------------
@patients_bp.route('/')
def index():
    return redirect(url_for('patients.list_patients'))

# ---------------- List Patients ----------------
@patients_bp.route('/patients')
def list_patients():
    patients = Patient.query.all()
    return render_template('patients.html', patients=patients)

# ---------------- Create Patient ----------------
@patients_bp.route('/patients/create', methods=['GET', 'POST'])
def create_patient():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form.get('birth_date')
        if not name:
            flash("Name is required!", "error")
            return redirect(url_for('patients.create_patient'))

        new_patient = Patient(name=name, birth_date=birth_date)
        db.session.add(new_patient)
        db.session.commit()
        flash("Patient created successfully!", "success")
        return redirect(url_for('patients.list_patients'))

    return render_template('create_patient.html')

# ---------------- Update Patient ----------------
@patients_bp.route('/patients/update/<int:patient_id>', methods=['GET', 'POST'])
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if request.method == 'POST':
        patient.name = request.form['name']
        patient.birth_date = request.form.get('birth_date')
        db.session.commit()
        flash("Patient updated successfully!", "success")
        return redirect(url_for('patients.list_patients'))

    return render_template('update_patient.html', patient=patient)

# ---------------- Delete Patient ----------------
@patients_bp.route('/patients/delete/<int:patient_id>', methods=['GET', 'POST'])
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if request.method == 'POST':
        db.session.delete(patient)
        db.session.commit()
        flash("Patient deleted successfully!", "success")
        return redirect(url_for('patients.list_patients'))

    # GET request mostra a página de confirmação
    return render_template('delete_patient.html', patient=patient)
