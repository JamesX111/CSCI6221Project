from flask import Blueprint, request, jsonify
from interfaces import SurgeryRecordService

bp = Blueprint("surgery", __name__, url_prefix="/api/surgeries")


# -------------------------------------------------------
# CREATE
# -------------------------------------------------------
@bp.route("/create", methods=["POST"])
def create_surgery_route():
    data = request.get_json()
    try:
        new_surgery = SurgeryRecordService.create_surgery(data)
        return jsonify(new_surgery), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# -------------------------------------------------------
# GET BY ID
# -------------------------------------------------------
@bp.route("/get/<int:surgery_id>", methods=["POST"])
def get_surgery_route(surgery_id):
    surgery = SurgeryRecordService.get_by_id(surgery_id)
    if surgery:
        return jsonify(surgery), 200
    return jsonify({"error": "Surgery not found"}), 404


# -------------------------------------------------------
# GET ALL
# -------------------------------------------------------
@bp.route("/get_all", methods=["POST"])
def get_all_surgeries_route():
    surgeries = SurgeryRecordService.get_all()
    return jsonify(surgeries), 200


# -------------------------------------------------------
# GET BY PATIENT
# -------------------------------------------------------
@bp.route("/get_by_patient/<int:patient_id>", methods=["POST"])
def get_by_patient_route(patient_id):
    surgeries = SurgeryRecordService.get_by_patient(patient_id)
    return jsonify(surgeries), 200


# -------------------------------------------------------
# GET BY DOCTOR / SURGEON
# -------------------------------------------------------
@bp.route("/get_by_doctor/<int:doctor_id>", methods=["POST"])
def get_by_doctor_route(doctor_id):
    surgeries = SurgeryRecordService.get_by_doctor(doctor_id)
    return jsonify(surgeries), 200


# -------------------------------------------------------
# GET BY NURSE
# -------------------------------------------------------
@bp.route("/get_by_nurse/<int:nurse_id>", methods=["POST"])
def get_by_nurse_route(nurse_id):
    surgeries = SurgeryRecordService.get_by_nurse(nurse_id)
    return jsonify(surgeries), 200


# -------------------------------------------------------
# GET BY HELPER
# -------------------------------------------------------
@bp.route("/get_by_helper/<int:helper_id>", methods=["POST"])
def get_by_helper_route(helper_id):
    surgeries = SurgeryRecordService.get_by_helper(helper_id)
    return jsonify(surgeries), 200


# -------------------------------------------------------
# GET BY SURGERY TYPE
# -------------------------------------------------------
@bp.route("/get_by_type/<string:surgery_type>", methods=["POST"])
def get_by_surgery_type_route(surgery_type):
    surgeries = SurgeryRecordService.get_by_surgery_type(surgery_type)
    return jsonify(surgeries), 200


# -------------------------------------------------------
# UPDATE
# -------------------------------------------------------
@bp.route("/update/<int:surgery_id>", methods=["PUT"])
def update_surgery_route(surgery_id):
    data = request.get_json()
    updated = SurgeryRecordService.update_surgery(surgery_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Surgery not found"}), 404


# -------------------------------------------------------
# DELETE
# -------------------------------------------------------
@bp.route("/delete/<int:surgery_id>", methods=["DELETE"])
def delete_surgery_route(surgery_id):
    success = SurgeryRecordService.delete_surgery(surgery_id)
    if success:
        return jsonify({"message": "Surgery deleted"}), 200
    return jsonify({"error": "Surgery not found"}), 404
