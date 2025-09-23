from flask import Blueprint, jsonify
from .models import Patient
from . import db

bp = Blueprint('main', __name__, url_prefix='/api')

@bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@bp.route('/patients', methods=['GET'])
def list_patients():
    patients = Patient.query.all()
    data = [{"id": p.id, "name": p.name} for p in patients]
    return jsonify(data), 200