from flask import Blueprint, request, jsonify
from interfaces import PatientService

bp = Blueprint("patients", __name__, url_prefix="/api/patients")


# ----------------------------------
# CREATE (create_patient)
# ----------------------------------
@bp.route("/create", methods=["POST"])
def create_patient_route():
    data = request.get_json()
    try:
        new_patient = PatientService.create_patient(data)
        return jsonify(new_patient), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ----------------------------------
# GET BY ID (get_patient_by_id)
# ----------------------------------
@bp.route("/get/<int:patient_id>", methods=["GET"])
def get_patient_by_id_route(patient_id):
    patient = PatientService.get_patient_by_id(patient_id)
    if patient:
        return jsonify(patient), 200
    return jsonify({"error": "Patient not found"}), 404


# ----------------------------------
# GET BY GENDER (get_patients_by_gender)
# ----------------------------------
@bp.route("/get_by_gender/<string:gender>", methods=["GET"])
def get_patients_by_gender_route(gender):
    patients = PatientService.get_patients_by_gender(gender)
    return jsonify(patients), 200


# ----------------------------------
# GET ALL (get_all_patients)
# ----------------------------------
@bp.route("/get_all", methods=["POST"])
def get_all_patients_route():
    patients = PatientService.get_all_patients()
    return jsonify(patients), 200


# ----------------------------------
# UPDATE (update_patient)
# ----------------------------------
@bp.route("/update/<int:patient_id>", methods=["PUT"])
def update_patient_route(patient_id):
    data = request.get_json()
    updated = PatientService.update_patient(patient_id, data)

    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Patient not found"}), 404


# ----------------------------------
# DELETE (delete_patient)
# ----------------------------------
@bp.route("/delete/<int:patient_id>", methods=["DELETE"])
def delete_patient_route(patient_id):
    success = PatientService.delete_patient(patient_id)

    if success:
        return jsonify({"message": "Patient deleted"}), 200
    return jsonify({"error": "Patient not found"}), 404
