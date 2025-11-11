
from flask import Blueprint, request, jsonify
from datetime import datetime


bp = Blueprint('hospital', __name__, url_prefix='/api/hospital')

# get all bedding based on hospital using data get from react frontend

@bp.route('/create_hospital', methods=['POST'])
def create_hospital():
    from db_util.hospital_util import create_hospital
    data = request.json
    try:
        hospital = create_hospital(data)
        print("here")
        return jsonify(hospital), 201
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400

@bp.route('/get_bedding', methods=['POST'])
def get_bedding():
    from db_model.hospital import Hospital
    with bp.app_context():
        data = request.json
        hospital_id = data.get("hospital_id")
        hospital = Hospital.query.filter_by(id=hospital_id).first()
        if hospital:
            bedding_info = {
                'has_emergency': hospital.has_emergency,
                'has_pediatrics': hospital.has_pediatrics,
                'has_cardiology': hospital.has_cardiology,
                'has_oncology': hospital.has_oncology,
                'has_neurology': hospital.has_neurology,
                'has_orthopedics': hospital.has_orthopedics,
                'has_radiology': hospital.has_radiology,
                'has_maternity': hospital.has_maternity,
            }
            return jsonify(bedding_info)
        else:
            return jsonify({"error": "Hospital not found"}), 404
        

# get all doctors based on hospital using data get from react frontend
@bp.route('/get_doctors', methods=['POST'])
def get_doctors():
    from db_model.doctor import Doctor
    with bp.app_context():
        data = request.json
        hospital_id = data.get("hospital_id")
        doctors = Doctor.query.filter_by(hospital_id=hospital_id).all()
        doctors_list = [doctor.to_dict() for doctor in doctors]
        return jsonify(doctors_list)
    
# get all hospitals
@bp.route('/get_all', methods=['POST'])
def get_hospitals():
    from db_model.hospital import Hospital
    hospitals = Hospital.query.all()
    hospitals_list = [hospital.to_dict() for hospital in hospitals]
    return jsonify(hospitals_list)

@bp.route('/get_hospital/<int:hospital_id>', methods=['POST'])
def get_hospital(hospital_id):
    from db_model.hospital import Hospital
    hospital = Hospital.query.get(hospital_id)
    if hospital:
        return jsonify(hospital.to_dict())
    else:
        return jsonify({"error": "Hospital not found"}), 404