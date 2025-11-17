from flask import Blueprint, request, jsonify
from interfaces import BedService

bp = Blueprint("beds", __name__, url_prefix="/api/beds")


# ----------------------------------
# CREATE (create_bed)
# ----------------------------------
@bp.route("/create", methods=["POST"])
def create_bed_route():
    data = request.get_json()
    try:
        new_bed = BedService.create_bed(data)
        return jsonify(new_bed), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ----------------------------------
# GET BY ID (get_bed_by_id)
# ----------------------------------
@bp.route("/get/<int:bed_no>", methods=["POST"])
def get_bed_by_id_route(bed_no):
    bed = BedService.get_bed_by_id(bed_no)
    if bed:
        return jsonify(bed), 200
    return jsonify({"error": "Bed not found"}), 404


# ----------------------------------
# GET BY WARD (get_beds_by_ward)
# ----------------------------------
@bp.route("/get_by_ward/<int:ward_no>", methods=["GET"])
def get_beds_by_ward_route(ward_no):
    beds = BedService.get_beds_by_ward(ward_no)
    return jsonify(beds), 200


# ----------------------------------
# GET ALL (get_all_beds)
# ----------------------------------
@bp.route("/get_all", methods=["POST"])
def get_all_beds_route():
    beds = BedService.get_all_beds()
    return jsonify(beds), 200


# ----------------------------------
# UPDATE (update_bed)
# ----------------------------------
@bp.route("/update/<int:bed_no>", methods=["PUT"])
def update_bed_route(bed_no):
    data = request.get_json()
    updated = BedService.update_bed(bed_no, data)

    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Bed not found"}), 404


# ----------------------------------
# DELETE (delete_bed)
# ----------------------------------
@bp.route("/delete/<int:bed_no>", methods=["DELETE"])
def delete_bed_route(bed_no):
    success = BedService.delete_bed(bed_no)

    if success:
        return jsonify({"message": "Bed deleted"}), 200
    return jsonify({"error": "Bed not found"}), 404
