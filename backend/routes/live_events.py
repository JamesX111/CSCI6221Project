# backend/routes/live_events.py

from flask import Blueprint, jsonify
from backend.simulation.live_simulation import ACTIVE_EVENTS

live_bp = Blueprint("live", __name__)

@live_bp.route("/live-events", methods=["GET"])
def get_live_events():
    # Returns an array of all active events
    return jsonify(list(ACTIVE_EVENTS.values()))

@live_bp.route("/live-events/<event_id>", methods=["GET"])
def get_live_event(event_id):
    ev = ACTIVE_EVENTS.get(event_id)
    if not ev:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(ev)
