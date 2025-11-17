from flask import Blueprint, request, jsonify
from db_model import Department

bp = Blueprint("departments", __name__, url_prefix="/api/departments")

@bp.route("/get_all",methods=["GET"])
def get_all():
    departments = Department.query.all()
    return [d.to_dict() for d in departments]