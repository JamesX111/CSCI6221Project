# backend/routes/live_events.py

import os
import sqlite3
from flask import Blueprint, jsonify
from backend.simulation.live_simulation import ACTIVE_EVENTS

live_bp = Blueprint("live", __name__)

# Resolve DB path relative to this file (backend/routes → ../../data)
DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "hospital_raw.db")
)


def _load_accepted_event_ids():
    """Return a set of event_ids that have been accepted."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=5.0)
        cur = conn.cursor()
        cur.execute("SELECT event_id FROM accepted_events")
        ids = {row[0] for row in cur.fetchall()}
        conn.close()
        return ids
    except Exception as e:
        print("[LIVE_EVENTS] Failed to load accepted_events:", e)
        return set()


@live_bp.route("/live-events", methods=["GET"])
def get_live_events():
    events = []
    accepted_ids = _load_accepted_event_ids()

    for ev in ACTIVE_EVENTS.values():
        eid = ev.get("event_id")

        events.append({
            **ev,
            "accepted": eid in accepted_ids,

            # ⭐ KEEP STAFF + BEDS AFTER REFRESH
            "assigned_staff": ev.get("assigned_staff", {
                "nurse": "N/A",
                "helper": "N/A"
            }),
            "accepted_beds": ev.get("accepted_beds", [])
        })

    return jsonify(events)



@live_bp.route("/live-events/<event_id>", methods=["GET"])
def get_live_event(event_id):
    ev = ACTIVE_EVENTS.get(event_id)
    if not ev:
        return jsonify({"error": "Event not found"}), 404

    accepted_ids = _load_accepted_event_ids()
    return jsonify({
        **ev,
        "accepted": event_id in accepted_ids,
        "assigned_staff": ev.get("assigned_staff", {
            "nurse": "N/A",
            "helper": "N/A"
        }),
        "accepted_beds": ev.get("accepted_beds", [])
    })

