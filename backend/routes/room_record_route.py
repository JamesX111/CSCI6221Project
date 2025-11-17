from flask import Blueprint, request, jsonify
from interfaces import RoomRecordService

bp = Blueprint("room_records", __name__, url_prefix="/api/room_records")


# -------------------------------------------------------
# CREATE  (create_record)
# -------------------------------------------------------
@bp.route("/create", methods=["POST"])
def create_record_route():
    data = request.get_json()
    try:
        new_record = RoomRecordService.create_record(data)
        return jsonify(new_record), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# -------------------------------------------------------
# GET BY ADMISSION ID (get_by_admission_id)
# -------------------------------------------------------
@bp.route("/get/<int:admission_id>", methods=["GET"])
def get_record_route(admission_id):
    record = RoomRecordService.get_by_admission_id(admission_id)
    if record:
        return jsonify(record), 200
    return jsonify({"error": "Record not found"}), 404


# -------------------------------------------------------
# GET ALL (get_all_records)
# -------------------------------------------------------
@bp.route("/get_all", methods=["GET"])
def get_all_records_route():
    records = RoomRecordService.get_all_records()
    return jsonify(records), 200


# -------------------------------------------------------
# GET BY PATIENT (get_by_patient)
# -------------------------------------------------------
@bp.route("/get_by_patient/<int:patient_id>", methods=["GET"])
def get_by_patient_route(patient_id):
    records = RoomRecordService.get_by_patient(patient_id)
    return jsonify(records), 200


# -------------------------------------------------------
# GET BY NURSE (get_by_nurse)
# -------------------------------------------------------
@bp.route("/get_by_nurse/<int:nurse_id>", methods=["GET"])
def get_by_nurse_route(nurse_id):
    records = RoomRecordService.get_by_nurse(nurse_id)
    return jsonify(records), 200


# -------------------------------------------------------
# GET BY HELPER (get_by_helper)
# -------------------------------------------------------
@bp.route("/get_by_helper/<int:helper_id>", methods=["GET"])
def get_by_helper_route(helper_id):
    records = RoomRecordService.get_by_helper(helper_id)
    return jsonify(records), 200


# -------------------------------------------------------
# GET BY ROOM NO (get_by_room_no)
# -------------------------------------------------------
@bp.route("/get_by_room/<int:room_no>", methods=["GET"])
def get_by_room_no_route(room_no):
    records = RoomRecordService.get_by_room_no(room_no)
    return jsonify(records), 200


# -------------------------------------------------------
# UPDATE (update_record)
# -------------------------------------------------------
@bp.route("/update/<int:admission_id>", methods=["PUT"])
def update_record_route(admission_id):
    data = request.get_json()
    updated = RoomRecordService.update_record(admission_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Record not found"}), 404


# -------------------------------------------------------
# DELETE (delete_record)
# -------------------------------------------------------
@bp.route("/delete/<int:admission_id>", methods=["DELETE"])
def delete_record_route(admission_id):
    success = RoomRecordService.delete_record(admission_id)
    if success:
        return jsonify({"message": "Record deleted"}), 200
    return jsonify({"error": "Record not found"}), 404
