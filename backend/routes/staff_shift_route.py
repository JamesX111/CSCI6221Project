from flask import Blueprint, request, jsonify
from interfaces import StaffShiftService

bp = Blueprint("shifts", __name__, url_prefix="/api/staff_shifts")


# -------------------------------------------------------
# CREATE (create_shift)
# -------------------------------------------------------
@bp.route("/create", methods=["POST"])
def create_shift_route():
    data = request.get_json()
    try:
        new_shift = StaffShiftService.create_shift(data)
        return jsonify(new_shift), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# -------------------------------------------------------
# GET BY ID (get_shift_by_id)
# -------------------------------------------------------
@bp.route("/get/<int:shift_id>", methods=["POST"])
def get_shift_route(shift_id):
    shift = StaffShiftService.get_shift_by_id(shift_id)
    if shift:
        return jsonify(shift), 200
    return jsonify({"error": "Shift not found"}), 404


# -------------------------------------------------------
# GET ALL (get_all_shifts)
# -------------------------------------------------------
@bp.route("/get_all", methods=["POST"])
def get_all_shifts_route():
    shifts = StaffShiftService.get_all_shifts()
    return jsonify(shifts), 200


# -------------------------------------------------------
# GET BY DOCTOR (get_by_doctor)
# -------------------------------------------------------
@bp.route("/get_by_doctor/<int:doct_id>", methods=["POST"])
def get_by_doctor_route(doct_id):
    shifts = StaffShiftService.get_by_doctor(doct_id)
    return jsonify(shifts), 200


# -------------------------------------------------------
# GET BY NURSE (get_by_nurse)
# -------------------------------------------------------
@bp.route("/get_by_nurse/<int:nurse_id>", methods=["POST"])
def get_by_nurse_route(nurse_id):
    shifts = StaffShiftService.get_by_nurse(nurse_id)
    return jsonify(shifts), 200


# -------------------------------------------------------
# GET BY HELPER (get_by_helper)
# -------------------------------------------------------
@bp.route("/get_by_helper/<int:helper_id>", methods=["POST"])
def get_by_helper_route(helper_id):
    shifts = StaffShiftService.get_by_helper(helper_id)
    return jsonify(shifts), 200


# -------------------------------------------------------
# UPDATE (update_shift)
# -------------------------------------------------------
@bp.route("/update/<int:shift_id>", methods=["PUT"])
def update_shift_route(shift_id):
    data = request.get_json()
    updated = StaffShiftService.update_shift(shift_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Shift not found"}), 404


# -------------------------------------------------------
# DELETE (delete_shift)
# -------------------------------------------------------
@bp.route("/delete/<int:shift_id>", methods=["DELETE"])
def delete_shift_route(shift_id):
    success = StaffShiftService.delete_shift(shift_id)
    if success:
        return jsonify({"message": "Shift deleted"}), 200
    return jsonify({"error": "Shift not found"}), 404
