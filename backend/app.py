# ===============================================================
# Proper Flask-SocketIO App Factory
# ===============================================================

import os
import sqlite3
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
from sqlalchemy import create_engine

# Global SocketIO object (app will be attached in create_app)
socketio = SocketIO()   # <-- NO app here


# ---------------------------------------------------------------
# APP FACTORY
# ---------------------------------------------------------------
def create_app():
    app = Flask(__name__)

    # --- Database path (shared everywhere) ---
    DB_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "data", "hospital_raw.db")
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DB_PATH"] = DB_PATH

    # --- CORS ---
    CORS(app)

    # --- SQLAlchemy base ---
    from backend.db_model import db
    db.init_app(app)

    # --- Small helper for simple SELECTs ---
    def read_table(query: str) -> pd.DataFrame:
        try:
            with sqlite3.connect(DB_PATH) as conn:
                df = pd.read_sql(query, conn)
            return df
        except Exception as e:
            print("[SQL ERROR]", e)
            return pd.DataFrame()

    # --- Blueprints (REST + live events) ---
    from backend.routes import event_bp
    from backend.routes.live_events import live_bp
    app.register_blueprint(event_bp, url_prefix="/api")
    app.register_blueprint(live_bp, url_prefix="/api")

    # -------------------------------------------------------
    #  LEGACY FRONTEND ENDPOINTS (Patients / Events / etc.)
    #  These match EXACTLY what the React app calls:
    #  /api/get_patients, /api/get_events, /api/get_bedding, ...
    # -------------------------------------------------------

    @app.route('/api/get_hospitals', methods=['GET', 'POST'])
    def get_hospitals():
        engine = create_engine(f"sqlite:///{DB_PATH}")
        query = """
            SELECT 
                dept_Id   AS id,
                dept_Name AS name,
                '-'       AS address,
                '-'       AS phone,
                '-'       AS email,
                '-'       AS departments
            FROM department
            LIMIT 50
        """
        df = pd.read_sql(query, engine)
        return jsonify(df.to_dict(orient='records'))

    @app.route("/api/get_doctors", methods=["GET", "POST"])
    def get_doctors():
        query = """
            SELECT DISTINCT 
                staff_name   AS doctor_name,
                role,
                shift_start,
                shift_end
            FROM staff_schedule
            LIMIT 50
        """
        df = read_table(query)
        return jsonify(df.to_dict(orient="records"))

    @app.route('/api/get_bedding', methods=['GET', 'POST'])
    def get_bedding():
        engine = create_engine(f"sqlite:///{DB_PATH}")
        query = """
            SELECT 
                bed_No  AS bed_id,
                ward_No AS ward,
                '-'     AS status,
                '-'     AS last_updated
            FROM bed
            LIMIT 100
        """
        df = pd.read_sql(query, engine)
        return jsonify(df.to_dict(orient='records'))

    @app.route('/api/get_events', methods=['GET', 'POST'])
    def get_events():
        engine = create_engine(f"sqlite:///{DB_PATH}")
        query = """
            SELECT 
                appoIntment_Id      AS id,
                patient_Id          AS patient,
                doct_Id             AS doctor,
                reason              AS description,
                appointment_Date    AS scheduled,
                appointment_status  AS status,
                mode_of_appointment AS type
            FROM appointment
            LIMIT 100
        """
        try:
            df = pd.read_sql(query, engine).fillna("-")
            return jsonify(df.to_dict(orient='records'))
        except Exception as e:
            print("[ERROR] /api/get_events failed:", e)
            return jsonify([])

    @app.route('/api/get_patients', methods=['GET', 'POST'])
    def get_patients():
        engine = create_engine(f"sqlite:///{DB_PATH}")
        query = """
            SELECT 
                patient_Id            AS id,
                FName || ' ' || LName AS name,
                email,
                contact_No            AS phone,
                Gender                AS gender,
                pt_Address            AS address
            FROM patients
            LIMIT 100
        """
        df = pd.read_sql(query, engine)
        return jsonify(df.to_dict(orient='records'))

    # ----------------- Forecasting endpoints -----------------

    @app.route("/api/forecast", methods=["GET"])
    def forecast_inflow():
        from implementation import forecast_inflow
        data = forecast_inflow(days_ahead=7)
        return jsonify(data.to_dict(orient="records"))

    @app.route("/api/forecast_summary", methods=["GET"])
    def forecast_summary():
        try:
            from implementation import forecast_inflow, generate_ai_summary
            horizon = request.args.get("days", default=7, type=int)
            if horizon not in [3, 7, 14, 30]:
                horizon = 7

            forecast_df = forecast_inflow(days_ahead=horizon)
            if forecast_df.empty:
                return jsonify({"forecast": [], "summary": "No data."})

            summary = generate_ai_summary(forecast_df)
            return jsonify({
                "forecast": forecast_df.to_dict(orient="records"),
                "summary": summary,
                "horizon": horizon,
            })
        except Exception as e:
            print("[ERROR] /api/forecast_summary failed:", e)
            return jsonify({"error": str(e), "forecast": [], "summary": "Error"})

    # ----------------- Socket.IO wiring -----------------

    @socketio.on("bed_update")
    def handle_bed_update(data):
        # this is still here in case you manually emit bed_update from somewhere
        socketio.emit("bed_update_event", data, broadcast=True)

    @app.route("/")
    def index():
        return jsonify({"message": "Hospital Management Backend is running."})

    # IMPORTANT: attach app to the global socketio here
    socketio.init_app(
        app,
        cors_allowed_origins="*",
        async_mode="eventlet",
    )

    return app
