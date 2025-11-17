from flask import Blueprint, request, jsonify
from interfaces import WardService

bp = Blueprint("ward", __name__, url_prefix="/api/wards")


# -------------------------------------------------------
# CREATE
# -------------------------------------------------------
@bp.route("/create", methods=["POST"])
def create_ward_route():
    data = request.get_json()
    try:
        new_ward = WardService.create_ward(data)
        return jsonify(new_ward), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# -------------------------------------------------------
# GET BY ID
# -------------------------------------------------------
@bp.route("/get/<int:ward_no>", methods=["POST"])
def get_ward_route(ward_no):
    ward = WardService.get_by_id(ward_no)
    if ward:
        return jsonify(ward), 200
    return jsonify({"error": "Ward not found"}), 404


# -------------------------------------------------------
# GET BY DEPARTMENT
# -------------------------------------------------------
@bp.route("/get_by_department/<int:dept_id>", methods=["POST"])
def get_by_department_route(dept_id):
    wards = WardService.get_by_department(dept_id)
    return jsonify(wards), 200


# -------------------------------------------------------
# GET ALL
# -------------------------------------------------------
@bp.route("/get_all", methods=["POST"])
def get_all_wards_route():
    wards = WardService.get_all()
    return jsonify(wards), 200


# -------------------------------------------------------
# UPDATE
# -------------------------------------------------------
@bp.route("/update/<int:ward_no>", methods=["PUT"])
def update_ward_route(ward_no):
    data = request.get_json()
    updated = WardService.update_ward(ward_no, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Ward not found"}), 404


# -------------------------------------------------------
# DELETE
# -------------------------------------------------------
@bp.route("/delete/<int:ward_no>", methods=["DELETE"])
def delete_ward_route(ward_no):
    success = WardService.delete_ward(ward_no)
    if success:
        return jsonify({"message": "Ward deleted"}), 200
    return jsonify({"error": "Ward not found"}), 404
