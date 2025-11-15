
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

@bp.route('/get_bedding/<int:hospital_id>', methods=['POST'])
def get_bedding(hospital_id):
    from db_model.hospital import Hospital
    from db_util.bed_util import get_beds_by_hospital
    hospital = Hospital.query.filter_by(id=hospital_id).first()
    if hospital:
        bedding_info = get_beds_by_hospital(hospital_id)
        return jsonify(bedding_info)
    else:
        return jsonify({"error": "Hospital not found"}), 404
        

# get all doctors based on hospital using data get from react frontend
@bp.route('/get_doctors/<int:hospital_id>', methods=['POST'])
def get_doctors(hospital_id):
    from db_model.doctor import Doctor
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
    

@bp.route('/update_hospital/<int:hospital_id>', methods=['PUT'])
def update_hospital(hospital_id):
    from db_model.hospital import Hospital
    from db_util.hospital_util import update_hospital
    data = request.json
    try:
        hospital = update_hospital(hospital_id, data)
        return jsonify(hospital), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400
    
@bp.route('/delete_hospital/<int:hospital_id>', methods=['DELETE'])
def delete_hospital(hospital_id):
    from db_model.hospital import Hospital
    from db_util.hospital_util import delete_hospital
    try:
        delete_hospital(hospital_id)
        return jsonify({"message": "Hospital deleted successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400


@bp.route('/create_bed/<int:hospital_id>', methods=['POST'])
def create_bed(hospital_id):
    print("call success")
    from db_util.bed_util import create_bed
    data = request.json
    data['hospital_id'] = hospital_id
    try:
        bed = create_bed(data)
        return jsonify(bed), 201
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400

@bp.route('/update_bed/<int:bed_id>', methods=['PUT'])
def update_bed(bed_id):
    from db_util.bed_util import update_bed
    data = request.json
    try:
        bed = update_bed(bed_id, data)
        return jsonify(bed), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400

@bp.route('/delete_bed/<int:bed_id>', methods=['DELETE'])
def delete_bed(bed_id):
    from db_util.bed_util import delete_bed
    try:
        result = delete_bed(bed_id)
        return jsonify(result), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400

@bp.route('/create_doctor/<int:hospital_id>', methods=['POST'])
def create_doctor(hospital_id):
    from db_util.doctor_util import create_doctor
    data = request.json
    data['hospital_id'] = hospital_id
    try:
        doctor = create_doctor(data)
        return jsonify(doctor), 201
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400

@bp.route('/update_doctor/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    from db_util.doctor_util import update_doctor
    data = request.json
    try:
        doctor = update_doctor(doctor_id, data)
        return jsonify(doctor), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400
    
@bp.route('/delete_doctor/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    from db_util.doctor_util import delete_doctor
    try:
        result = delete_doctor(doctor_id)
        return jsonify(result), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400

@bp.route('/get_bed/<int:bed_id>', methods=['POST'])
def get_bed(bed_id):
    from db_util.bed_util import get_bed
    try:
        bed = get_bed(bed_id)
        return jsonify(bed), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400
    

@bp.route('/get_doctor/<int:doctor_id>', methods=['POST'])
def get_doctor(doctor_id):
    from db_util.doctor_util import get_doctor
    try:
        doctor = get_doctor(doctor_id)
        return jsonify(doctor), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400