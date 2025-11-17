# backend/run.py

import eventlet
eventlet.monkey_patch()

from backend.app import create_app, socketio
from backend.simulation.live_simulation import init_simulation

# 1) Create the Flask app (and init SocketIO inside create_app)
app = create_app()

# 2) Start the background real-time simulation
init_simulation(app, socketio)

# 3) Run Flask-SocketIO server
if __name__ == "__main__":
    print(">>> Starting REAL Socket.IO server (eventlet mode)")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
