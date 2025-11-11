
from flask import Blueprint, request, jsonify
from datetime import datetime
from db_model import Event, db
from db_util import event_util

bp = Blueprint('events', __name__, url_prefix='/api/events')

@bp.route('/create_event', methods=['POST'])
def create_event():
    data = request.json
    event = event_util.create_event(data)
    return jsonify(event.to_dict()), 201
