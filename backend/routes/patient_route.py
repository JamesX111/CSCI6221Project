
from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.db_util import patient_util


bp = Blueprint('patient', __name__, url_prefix='/api/patient')

# get all patients
@bp.route('/get_all', methods=['POST'])
def get_all_patients():
    return jsonify(patient_util.get_all_patients())