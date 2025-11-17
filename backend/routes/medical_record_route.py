from flask import Blueprint, request, jsonify
from interfaces import MedicalRecordService

bp = Blueprint("medical_records", __name__, url_prefix="/api/medical_records")


# ----------------------------------
# CREATE (create_medical_record)
# ----------------------------------
@bp.route("/create", methods=["POST"])
def create_medical_record_route():
    data = request.get_json()
    try:
        new_record = MedicalRecordService.create_medical_record(data)
        return jsonify(new_record), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ----------------------------------
# GET BY ID (get_medical_record_by_id)
# ----------------------------------
@bp.route("/get/<int:record_id>", methods=["GET"])
def get_medical_record_by_id_route(record_id):
    record = MedicalRecordService.get_medical_record_by_id(record_id)
    if record:
        return jsonify(record), 200
    return jsonify({"error": "Medical record not found"}), 404


# ----------------------------------
# GET BY DOCTOR (get_medical_records_by_doctor)
# ----------------------------------
@bp.route("/get_by_doctor/<int:doct_id>", methods=["GET"])
def get_records_by_doctor_route(doct_id):
    records = MedicalRecordService.get_medical_records_by_doctor(doct_id)
    return jsonify(records), 200


# ----------------------------------
# GET BY PATIENT (get_medical_records_by_patient)
# ----------------------------------
@bp.route("/get_by_patient/<int:patient_id>", methods=["GET"])
def get_records_by_patient_route(patient_id):
    records = MedicalRecordService.get_medical_records_by_patient(patient_id)
    return jsonify(records), 200


# ----------------------------------
# GET ALL (get_all_medical_records)
# ----------------------------------
@bp.route("/get_all", methods=["GET"])
def get_all_medical_records_route():
    records = MedicalRecordService.get_all_medical_records()
    return jsonify(records), 200


# ----------------------------------
# UPDATE (update_medical_record)
# ----------------------------------
@bp.route("/update/<int:record_id>", methods=["PUT"])
def update_medical_record_route(record_id):
    data = request.get_json()
    updated = MedicalRecordService.update_medical_record(record_id, data)

    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Medical record not found"}), 404


# ----------------------------------
# DELETE (delete_medical_record)
# ----------------------------------
@bp.route("/delete/<int:record_id>", methods=["DELETE"])
def delete_medical_record_route(record_id):
    success = MedicalRecordService.delete_medical_record(record_id)

    if success:
        return jsonify({"message": "Medical record deleted"}), 200
    return jsonify({"error": "Medical record not found"}), 404
