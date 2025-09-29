from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from .models import db, Patient

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/patients')
@login_required
def list_patients():
    patients = Patient.query.all()
    return render_template('patients.html', patients=patients)

@patients_bp.route('/patients/add', methods=['GET', 'POST'])
@login_required
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        condition = request.form['condition']

        new_patient = Patient(name=name, age=age, condition=condition)
        db.session.add(new_patient)
        db.session.commit()

        flash('Patient added successfully!', 'success')
        return redirect(url_for('patients.list_patients'))

    return render_template('add_patient.html')

@patients_bp.route('/patients/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_patient(id):
    patient = Patient.query.get_or_404(id)

    if request.method == 'POST':
        patient.name = request.form['name']
        patient.age = request.form['age']
        patient.condition = request.form['condition']

        db.session.commit()
        flash('Patient updated successfully!', 'success')
        return redirect(url_for('patients.list_patients'))

    return render_template('edit_patient.html', patient=patient)

@patients_bp.route('/patients/<int:id>/delete', methods=['POST'])
@login_required
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient deleted successfully!', 'info')
    return redirect(url_for('patients.list_patients'))
