from flask import Blueprint, request, jsonify
from interfaces import RoomService

bp = Blueprint("rooms", __name__, url_prefix="/api/rooms")


# -------------------------------------------------------
# CREATE  (create_room)
# -------------------------------------------------------
@bp.route("/create", methods=["POST"])
def create_room_route():
    data = request.get_json()
    try:
        new_room = RoomService.create_room(data)
        return jsonify(new_room), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# -------------------------------------------------------
# GET BY ROOM NO (get_room_by_id)
# -------------------------------------------------------
@bp.route("/get/<int:room_no>", methods=["GET"])
def get_room_route(room_no):
    room = RoomService.get_room_by_id(room_no)
    if room:
        return jsonify(room), 200
    return jsonify({"error": "Room not found"}), 404


# -------------------------------------------------------
# GET ALL (get_all_rooms)
# -------------------------------------------------------
@bp.route("/get_all", methods=["GET"])
def get_all_rooms_route():
    rooms = RoomService.get_all_rooms()
    return jsonify(rooms), 200


# -------------------------------------------------------
# GET BY DEPARTMENT (get_rooms_by_department)
# -------------------------------------------------------
@bp.route("/get_by_department/<int:dept_id>", methods=["GET"])
def get_by_department_route(dept_id):
    rooms = RoomService.get_rooms_by_department(dept_id)
    return jsonify(rooms), 200


# -------------------------------------------------------
# GET BY ROOM TYPE (get_rooms_by_type)
# -------------------------------------------------------
@bp.route("/get_by_type/<room_type>", methods=["GET"])
def get_by_type_route(room_type):
    rooms = RoomService.get_rooms_by_type(room_type)
    return jsonify(rooms), 200


# -------------------------------------------------------
# UPDATE (update_room)
# -------------------------------------------------------
@bp.route("/update/<int:room_no>", methods=["PUT"])
def update_room_route(room_no):
    data = request.get_json()
    updated = RoomService.update_room(room_no, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({"error": "Room not found"}), 404


# -------------------------------------------------------
# DELETE (delete_room)
# -------------------------------------------------------
@bp.route("/delete/<int:room_no>", methods=["DELETE"])
def delete_room_route(room_no):
    success = RoomService.delete_room(room_no)
    if success:
        return jsonify({"message": "Room deleted"}), 200
    return jsonify({"error": "Room not found"}), 404
