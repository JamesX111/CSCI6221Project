
from flask import Blueprint, request, jsonify
from datetime import datetime
from db_model import Event, db
from db_util import event_util

bp = Blueprint('accidents', __name__, url_prefix='/api/accidents')

@bp.route('/get_all', methods=['POST'])
def get_all():
    from db_model.accident import Accident
    accidents = Accident.query.all()
    accidents_list = [accident.to_dict() for accident in accidents]
    return jsonify(accidents_list)
    
@bp.route('/create_accident', methods=['POST'])
def create_accident():
    data = request.json
    try:
        from db_util.accident_util import create_accident
        accident = create_accident(data)
        return jsonify(accident.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/update_accident/<int:accident_id>', methods=['PUT'])
def update_accident(accident_id):
    data = request.json
    try:
        from db_util.accident_util import update_accident
        accident = update_accident(accident_id, data)
        return jsonify(accident), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@bp.route('/get_accident/<int:accident_id>', methods=['POST'])
def get_accident(accident_id):
    try:
        from db_util.accident_util import get_accident_by_id
        accident = get_accident_by_id(accident_id)
        return jsonify(accident), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/delete_accident/<int:accident_id>', methods=['DELETE'])
def delete_accident(accident_id):
    try:
        from db_model.accident import Accident
        accident = Accident.query.get(accident_id)
        if not accident:
            return jsonify({"error": f"Accident with ID {accident_id} not found."}), 404
        db.session.delete(accident)
        db.session.commit()
        return jsonify({"message": f"Accident with ID {accident_id} deleted."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400