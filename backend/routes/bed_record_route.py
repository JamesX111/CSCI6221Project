from flask import Blueprint, request, jsonify
from interfaces import BedRecordService

bp = Blueprint("bed_records", __name__, url_prefix="/api/bed_records")


# ----------------------------------
# CREATE (create_bed_record)
# ----------------------------------
@bp.route("/create", methods=["POST"])
def create_bed_record_route():
    data = request.get_json()
    try:
        new_record = BedRecordService.create_bed_record(data)
        return jsonify(new_record), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ----------------------------------
# GET ALL (get_all_bed_records)
# ----------------------------------
@bp.route("/get_all", methods=["POST"])
def get_all_bed_records_route():
    records = BedRecordService.get_all_bed_records()
    return jsonify(records), 200


# ----------------------------------
# GET BY ID (same as admission_Id)
# ----------------------------------
@bp.route("/get/<int:admission_id>", methods=["POST"])
def get_bed_record_by_id_route(admission_id):
    record = BedRecordService.get_bed_record_by_id(admission_id) \
        if hasattr(BedRecordService, "get_bed_record_by_id") else None

    # If service has no get_by_id, manually fetch it:
    if record is None:
        from db_model import BedRecord
        r = BedRecord.query.get(admission_id)
        record = r.to_dict() if r else None

    if record:
        return jsonify(record), 200
    return jsonify({"error": "Bed record not found"}), 404


# ----------------------------------
# GET BY BED (get_records_by_bed)
# ----------------------------------
@bp.route("/get_by_bed/<int:bed_no>", methods=["POST"])
def get_records_by_bed_route(bed_no):
    records = BedRecordService.get_records_by_bed(bed_no)
    return jsonify(records), 200


# ----------------------------------
# GET BY PATIENT (get_records_by_patient)
# ----------------------------------
@bp.route("/get_by_patient/<int:patient_id>", methods=["POST"])
def get_records_by_patient_route(patient_id):
    records = BedRecordService.get_records_by_patient(patient_id)
    return jsonify(records), 200


# ----------------------------------
# GET BY NURSE (get_records_by_nurse)
# ----------------------------------
@bp.route("/get_by_nurse/<int:nurse_id>", methods=["POST"])
def get_records_by_nurse_route(nurse_id):
    records = BedRecordService.get_records_by_nurse(nurse_id)
    return jsonify(records), 200


# ----------------------------------
# GET BY HELPER (get_records_by_helper)
# ----------------------------------
@bp.route("/get_by_helper/<int:helper_id>", methods=["POST"])
def get_records_by_helper_route(helper_id):
    records = BedRecordService.get_records_by_helper(helper_id)
    return jsonify(records), 200


# ----------------------------------
# UPDATE (update_bed_record)
# ----------------------------------
@bp.route("/update/<int:admission_id>", methods=["PUT"])
def update_bed_record_route(admission_id):
    data = request.get_json()
    updated = BedRecordService.update_bed_record(admission_id, data)

    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Bed record not found"}), 404


# ----------------------------------
# DELETE (delete_bed_record)
# ----------------------------------
@bp.route("/delete/<int:admission_id>", methods=["DELETE"])
def delete_bed_record_route(admission_id):
    success = BedRecordService.delete_bed_record(admission_id)

    if success:
        return jsonify({"message": "Bed record deleted"}), 200
    return jsonify({"error": "Bed record not found"}), 404
