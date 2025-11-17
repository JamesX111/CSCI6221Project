from flask import Blueprint, request, jsonify
from interfaces import HelperService

bp = Blueprint("helpers", __name__, url_prefix="/api/helpers")


# ----------------------------------
# CREATE (create_helper)
# ----------------------------------
@bp.route("/create", methods=["POST"])
def create_helper_route():
    data = request.get_json()
    try:
        new_helper = HelperService.create_helper(data)
        return jsonify(new_helper), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ----------------------------------
# GET BY ID (get_helper_by_id)
# ----------------------------------
@bp.route("/get/<int:helper_id>", methods=["GET"])
def get_helper_by_id_route(helper_id):
    helper = HelperService.get_helper_by_id(helper_id)
    if helper:
        return jsonify(helper), 200
    return jsonify({"error": "Helper not found"}), 404


# ----------------------------------
# GET BY GENDER (get_helpers_by_gender)
# ----------------------------------
@bp.route("/get_by_gender/<string:gender>", methods=["GET"])
def get_helpers_by_gender_route(gender):
    helpers = HelperService.get_helpers_by_gender(gender)
    return jsonify(helpers), 200


# ----------------------------------
# GET BY DEPARTMENT (get_helpers_by_department)
# ----------------------------------
@bp.route("/get_by_department/<int:dept_id>", methods=["GET"])
def get_helpers_by_department_route(dept_id):
    helpers = HelperService.get_helpers_by_department(dept_id)
    return jsonify(helpers), 200


# ----------------------------------
# GET ALL (get_all_helpers)
# ----------------------------------
@bp.route("/get_all", methods=["GET"])
def get_all_helpers_route():
    helpers = HelperService.get_all_helpers()
    return jsonify(helpers), 200


# ----------------------------------
# UPDATE (update_helper)
# ----------------------------------
@bp.route("/update/<int:helper_id>", methods=["PUT"])
def update_helper_route(helper_id):
    data = request.get_json()
    updated = HelperService.update_helper(helper_id, data)

    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Helper not found"}), 404


# ----------------------------------
# DELETE (delete_helper)
# ----------------------------------
@bp.route("/delete/<int:helper_id>", methods=["DELETE"])
def delete_helper_route(helper_id):
    success = HelperService.delete_helper(helper_id)

    if success:
        return jsonify({"message": "Helper deleted"}), 200
    return jsonify({"error": "Helper not found"}), 404
