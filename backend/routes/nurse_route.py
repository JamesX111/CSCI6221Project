from flask import Blueprint, request, jsonify
from interfaces import NurseService

bp = Blueprint("nurses", __name__, url_prefix="/api/nurses")


# ----------------------------------
# CREATE (create_nurse)
# ----------------------------------
@bp.route("/create", methods=["POST"])
def create_nurse_route():
    data = request.get_json()
    try:
        new_nurse = NurseService.create_nurse(data)
        return jsonify(new_nurse), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ----------------------------------
# GET BY ID (get_nurse_by_id)
# ----------------------------------
@bp.route("/get/<int:nurse_id>", methods=["GET"])
def get_nurse_by_id_route(nurse_id):
    nurse = NurseService.get_nurse_by_id(nurse_id)
    if nurse:
        return jsonify(nurse), 200
    return jsonify({"error": "Nurse not found"}), 404


# ----------------------------------
# GET BY GENDER (get_nurses_by_gender)
# ----------------------------------
@bp.route("/get_by_gender/<string:gender>", methods=["GET"])
def get_nurses_by_gender_route(gender):
    nurses = NurseService.get_nurses_by_gender(gender)
    return jsonify(nurses), 200


# ----------------------------------
# GET BY DEPARTMENT (get_nurses_by_department)
# ----------------------------------
@bp.route("/get_by_department/<int:dept_id>", methods=["GET"])
def get_nurses_by_department_route(dept_id):
    nurses = NurseService.get_nurses_by_department(dept_id)
    return jsonify(nurses), 200


# ----------------------------------
# GET ALL (get_all_nurses)
# ----------------------------------
@bp.route("/get_all", methods=["POST"])
def get_all_nurses_route():
    nurses = NurseService.get_all_nurses()
    return jsonify(nurses), 200


# ----------------------------------
# UPDATE (update_nurse)
# ----------------------------------
@bp.route("/update/<int:nurse_id>", methods=["PUT"])
def update_nurse_route(nurse_id):
    data = request.get_json()
    updated = NurseService.update_nurse(nurse_id, data)

    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Nurse not found"}), 404


# ----------------------------------
# DELETE (delete_nurse)
# ----------------------------------
@bp.route("/delete/<int:nurse_id>", methods=["DELETE"])
def delete_nurse_route(nurse_id):
    success = NurseService.delete_nurse(nurse_id)

    if success:
        return jsonify({"message": "Nurse deleted"}), 200
    return jsonify({"error": "Nurse not found"}), 404
