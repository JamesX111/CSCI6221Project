
from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.db_model import db
from backend.db_model.event import Event
from backend.db_util import event_util

bp = Blueprint('events', __name__, url_prefix='/api/events')

@bp.route('/create_event', methods=['POST'])
def create_event():
    data = request.json
    event = event_util.create_event(data)
    return jsonify(event.to_dict()), 201

@bp.route('/get_all', methods=['GET'])
def get_all_events():
    events = Event.query.all()
    return jsonify([e.to_dict() for e in events]), 200