
from flask import Blueprint, request, jsonify
from datetime import datetime
from db_model import Event, db
from db_util import event_util

bp = Blueprint('events', __name__, url_prefix='/api/events')

@bp.route('/create_event', methods=['POST'])
def create_event():
    data = request.json
    try:
        event = event_util.create_event(data)
        return jsonify(event), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# get all events
@bp.route('/get_all', methods=['POST'])
def get_events():
    from db_model.event import Event
    events = Event.query.all()
    events_list = [event.to_dict() for event in events]
    return jsonify(events_list)

@bp.route('/update_event/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.json
    try:
        event = event_util.update_event(event_id, data)
        return jsonify(event), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/get_event/<int:event_id>', methods=['POST'])
def get_event(event_id):
    try:
        event = event_util.get_event(event_id)
        return jsonify(event), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/delete_event/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    try:
        from db_model.event import Event
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": f"Event with ID {event_id} not found."}), 404
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": f"Event with ID {event_id} deleted."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400