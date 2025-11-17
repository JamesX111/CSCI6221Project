from flask import Blueprint, request, jsonify
from interfaces import AppointmentService

bp = Blueprint("appointments", __name__, url_prefix="/api/appointments")


# ---------------------------
# CREATE (create_appointment)
# ---------------------------
@bp.route("/create", methods=["POST"])
def create_appointment_route():
    data = request.get_json()
    try:
        new_appt = AppointmentService.create_appointment(data)
        return jsonify(new_appt), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ---------------------------
# GET ALL (get_all_appointments)
# ---------------------------
@bp.route("/get_all", methods=["GET"])
def get_all_appointments_route():
    appointments = AppointmentService.get_all_appointments()
    return jsonify(appointments), 200


# ---------------------------
# GET BY ID (get_appointment_by_id)
# ---------------------------
@bp.route("/get/<int:appointment_id>", methods=["GET"])
def get_appointment_by_id_route(appointment_id):
    appointment = AppointmentService.get_appointment_by_id(appointment_id)
    if appointment:
        return jsonify(appointment), 200
    return jsonify({"error": "Appointment not found"}), 404


# ---------------------------
# GET BY PATIENT (get_appointments_by_patient)
# ---------------------------
@bp.route("/get_by_patient/<int:patient_id>", methods=["GET"])
def get_by_patient_route(patient_id):
    appointments = AppointmentService.get_appointments_by_patient(patient_id)
    return jsonify(appointments), 200


# ---------------------------
# GET BY DOCTOR (get_appointments_by_doctor)
# ---------------------------
@bp.route("/get_by_doctor/<int:doctor_id>", methods=["GET"])
def get_by_doctor_route(doctor_id):
    appointments = AppointmentService.get_appointments_by_doctor(doctor_id)
    return jsonify(appointments), 200


# ---------------------------
# UPDATE (update_appointment)
# ---------------------------
@bp.route("/update/<int:appointment_id>", methods=["PUT"])
def update_appointment_route(appointment_id):
    data = request.get_json()
    updated = AppointmentService.update_appointment(appointment_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Appointment not found"}), 404


# ---------------------------
# DELETE (delete_appointment)
# ---------------------------
@bp.route("/delete/<int:appointment_id>", methods=["DELETE"])
def delete_appointment_route(appointment_id):
    success = AppointmentService.delete_appointment(appointment_id)
    if success:
        return jsonify({"message": "Appointment deleted"}), 200
    return jsonify({"error": "Appointment not found"}), 404
