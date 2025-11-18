# backend/simulation/live_simulation.py

import time
import os
import uuid
import threading

from backend.simulation.real_time_events import RealTimeEventGenerator, event_to_dict
from backend.simulation.resource_optimizer import ResourceOptimizer

# Active events dictionary that the REST API can read
ACTIVE_EVENTS = {}

# These are set by init_simulation() from run.py
app = None
socketio = None


def init_simulation(flask_app, sio):
    """
    Called AFTER create_app() in run.py.
    Stores the app + socketio and starts the background simulation thread.
    """
    global app, socketio
    app = flask_app
    socketio = sio

    t = threading.Thread(target=_simulation_loop, daemon=True)
    t.start()


def broadcast_update(event, predicted, allocations, summary):
    """
    Broadcasts a simulation update via Socket.IO and keeps a copy
    in ACTIVE_EVENTS for the /api/live-events endpoints.
    """
    formatted_alloc = [
        {"patient_id": p, "bed_id": b}
        for p, b in allocations
    ]

    payload = {
        "event_id": event["event_id"],
        "event": event,
        "predicted": predicted,
        "allocations": formatted_alloc,
        "summary": summary,
    }

    # Store for REST access
    ACTIVE_EVENTS[event["event_id"]] = payload

    # Emit over WebSocket
    if socketio:
        socketio.emit("simulation_update", payload)


def _simulation_loop():
    """
    Runs the real-time simulation in a background thread.
    Uses app.app_context() to safely access configuration if needed.
    Simulation is now READ-ONLY with respect to the database.
    """
    global app, socketio

    if app is None or socketio is None:
        print("[ERROR] Simulation started before init_simulation()")
        return

    gen = RealTimeEventGenerator()
    optimizer = ResourceOptimizer()

    with app.app_context():
        print(">>> Background real-time simulation started...")
        time.sleep(1)

        while True:
            # 1) Generate event
            evt = gen.generate_event()
            evt_dict = event_to_dict(evt)
            evt_dict["event_id"] = str(uuid.uuid4())

            # 2) Forecast patients and SUGGEST resources (no writes)
            predicted = optimizer.forecast_patients(evt_dict)
            allocations = optimizer.allocate_resources(predicted)
            summary = optimizer.ai_summary(evt_dict, predicted, allocations)

            # 3) Broadcast + (optionally) print to console
            broadcast_update(evt_dict, predicted, allocations, summary)
            _print_dashboard(evt_dict, predicted, allocations, summary)

            # 4) Wait until next “accident”
            gen.random_wait(0, 5)


# ---------- Optional console view (for your terminal demo) ----------

def _clear():
    os.system("cls" if os.name == "nt" else "clear")


def _print_dashboard(event, predicted, allocations, ai_text):
    _clear()
    print("===============================================")
    print("      REAL-TIME HOSPITAL OPERATIONS SYSTEM     ")
    print("===============================================\n")

    print(f"Event: {event['event_type']}  (Severity: {event['severity']})")
    print(f"Location: {event['location']}")
    print(f"Predicted Incoming Patients: {predicted}\n")

    admitted = sum(1 for _, b in allocations if b is not None)
    waiting = sum(1 for _, b in allocations if b is None)

    print(f"Patients Assigned Beds (simulated): {admitted}")
    print(f"Patients Waiting (simulated): {waiting}\n")

    print("AI Summary:")
    print("-----------------------------------------------")
    print(ai_text)
    print("-----------------------------------------------\n")
