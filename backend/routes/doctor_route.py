from flask import Blueprint, request, jsonify
from interfaces import DoctorService

bp = Blueprint("doctors", __name__, url_prefix="/api/doctors")


# ----------------------------------
# CREATE (create_doctor)
# ----------------------------------
@bp.route("/create", methods=["POST"])
def create_doctor_route():
    data = request.get_json()
    try:
        new_doctor = DoctorService.create_doctor(data)
        return jsonify(new_doctor), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ----------------------------------
# GET BY ID (get_doctor_by_id)
# ----------------------------------
@bp.route("/get/<int:doctor_id>", methods=["GET"])
def get_doctor_by_id_route(doctor_id):
    doctor = DoctorService.get_doctor_by_id(doctor_id)
    if doctor:
        return jsonify(doctor), 200
    return jsonify({"error": "Doctor not found"}), 404


# ----------------------------------
# GET BY GENDER (get_doctors_by_gender)
# ----------------------------------
@bp.route("/get_by_gender/<string:gender>", methods=["GET"])
def get_doctors_by_gender_route(gender):
    doctors = DoctorService.get_doctors_by_gender(gender)
    return jsonify(doctors), 200


# ----------------------------------
# GET BY DEPARTMENT (get_doctors_by_department)
# ----------------------------------
@bp.route("/get_by_department/<int:dept_id>", methods=["GET"])
def get_doctors_by_department_route(dept_id):
    doctors = DoctorService.get_doctors_by_department(dept_id)
    return jsonify(doctors), 200


# ----------------------------------
# GET ALL (get_all_doctors)
# ----------------------------------
@bp.route("/get_all", methods=["POST"])
def get_all_doctors_route():
    doctors = DoctorService.get_all_doctors()
    return jsonify(doctors), 200


# ----------------------------------
# UPDATE (update_doctor)
# ----------------------------------
@bp.route("/update/<int:doctor_id>", methods=["PUT"])
def update_doctor_route(doctor_id):
    data = request.get_json()
    updated = DoctorService.update_doctor(doctor_id, data)

    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Doctor not found"}), 404


# ----------------------------------
# DELETE (delete_doctor)
# ----------------------------------
@bp.route("/delete/<int:doctor_id>", methods=["DELETE"])
def delete_doctor_route(doctor_id):
    success = DoctorService.delete_doctor(doctor_id)

    if success:
        return jsonify({"message": "Doctor deleted"}), 200
    return jsonify({"error": "Doctor not found"}), 404
