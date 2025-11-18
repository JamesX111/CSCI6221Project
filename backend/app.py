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

# rotation indices (global in this module)
NURSE_INDEX = 0
HELPER_INDEX = 0

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

    # Ensure accepted_events table exists (schema WITHOUT 'accepted' column)
    with sqlite3.connect(DB_PATH, timeout=5.0) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS accepted_events (
                event_id TEXT PRIMARY KEY,
                event_type TEXT,
                severity INTEGER,
                location TEXT,
                patients_expected INTEGER,
                patients_assigned INTEGER,
                assigned_beds TEXT,
                assigned_staff TEXT,
                accepted_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

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

    # -----------------------------------------------------------
    # Accept an event: this is the ONLY place we write for live events
    # -----------------------------------------------------------
    @app.route('/api/accept_event', methods=['POST'])
    def accept_event():
        """
        Officially accept a simulated event, assign:
        - beds
        - one nurse
        - one helper
        Save results permanently and update ACTIVE_EVENTS.
        """
        from backend.simulation.live_simulation import ACTIVE_EVENTS

        data = request.json
        event_id = data["event_id"]
        num_patients = int(data["patients"])
        severity = int(data["severity"])
        event_type = data["event_type"]
        location = data["location"]

        conn = sqlite3.connect(DB_PATH, timeout=10)
        cursor = conn.cursor()

        # -----------------------
        # 1. Find free beds
        # -----------------------
        cursor.execute("""
            SELECT bed_No 
            FROM bed 
            WHERE bed_No NOT IN (
                SELECT bed_No FROM bedrecords WHERE discharge_Date IS NULL
            )
            LIMIT ?
        """, (num_patients,))
        free_beds = [row[0] for row in cursor.fetchall()]

        if len(free_beds) < num_patients:
            return jsonify({"error": "Not enough beds"}), 400

        # -----------------------
        # 2. Pick nurse + helper (ROTATING STAFF)
        # -----------------------
        global NURSE_INDEX, HELPER_INDEX

        # Fetch all nurses
        cursor.execute("SELECT nurse_Id, FName || ' ' || LName FROM nurse ORDER BY nurse_Id")
        nurses = cursor.fetchall()

        cursor.execute("SELECT helper_Id, FName || ' ' || LName FROM helpers ORDER BY helper_Id")
        helpers = cursor.fetchall()

        # Assign nurse
        if nurses:
            nurse_row = nurses[NURSE_INDEX % len(nurses)]
            nurse_id, nurse_name = nurse_row
            NURSE_INDEX += 1
        else:
            nurse_id, nurse_name = None, "N/A"

        # Assign helper
        if helpers:
            helper_row = helpers[HELPER_INDEX % len(helpers)]
            helper_id, helper_name = helper_row
            HELPER_INDEX += 1
        else:
            helper_id, helper_name = None, "N/A"


        # -----------------------
        # 3. Create patients + insert admissions in ONE transaction
        # -----------------------
        assigned_patients = []
        assigned_beds = []

        for bed_no in free_beds:
            cursor.execute("""
                INSERT INTO patients(FName, LName, Gender, contact_No, pt_Address, email, Date_Of_Birth)
                VALUES ('Unknown', 'Patient', 'Unknown', '', '', '', '1990-01-01')
            """)
            pid = cursor.lastrowid

            cursor.execute("""
                INSERT INTO bedrecords(bed_No, patient_Id, nurse_Id, helper_Id, admission_Date, discharge_Date)
                VALUES (?, ?, ?, ?, datetime('now'), NULL)
            """, (bed_no, pid, nurse_id, helper_id))

            assigned_patients.append(pid)
            assigned_beds.append(bed_no)

        # -----------------------
        # 4. Save accepted event
        # -----------------------
        cursor.execute("""
            INSERT OR REPLACE INTO accepted_events(
                event_id, event_type, severity, location,
                patients_expected, patients_assigned,
                assigned_beds, assigned_staff,
                accepted, accepted_timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, CURRENT_TIMESTAMP)
        """, (
            event_id, event_type, severity, location,
            num_patients, len(assigned_patients),
            ",".join(map(str, assigned_beds)),
            f"Nurse: {nurse_name} | Helper: {helper_name}"
        ))

        conn.commit()
        conn.close()

        # -----------------------
        # 5. Update ACTIVE_EVENTS (frontend state won't RESET)
        # -----------------------
        if event_id in ACTIVE_EVENTS:
            ACTIVE_EVENTS[event_id]["accepted"] = True
            ACTIVE_EVENTS[event_id]["assigned_staff"] = {
                "nurse": nurse_name,
                "helper": helper_name
            }
            ACTIVE_EVENTS[event_id]["accepted_beds"] = assigned_beds

        # -----------------------
        # 6. Emit update
        # -----------------------
        socketio.emit("bed_update_event", {
            "event_id": event_id,
            "accepted": True,
            "assigned_beds": assigned_beds,
            "patients_assigned": len(assigned_patients),
            "nurse": nurse_name,
            "helper": helper_name
        })

        return jsonify({
            "success": True,
            "accepted": True,
            "assigned_beds": assigned_beds,
            "patients": assigned_patients,
            "nurse": nurse_name,
            "helper": helper_name
        })




    # -----------------------------------------------------------
    # HOSPITAL / RESOURCES ENDPOINTS
    # -----------------------------------------------------------
    @app.route('/api/get_hospitals', methods=['GET'])
    def get_hospitals():
        conn = sqlite3.connect(DB_PATH)
        query = """
            SELECT
                id,
                name,
                address,
                phone,
                email,

                (has_emergency +
                has_pediatrics +
                has_cardiology +
                has_oncology +
                has_neurology +
                has_orthopedics +
                has_radiology +
                has_maternity) AS departments

            FROM hospital
            LIMIT 50
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return jsonify(df.to_dict(orient="records"))

    @app.route('/api/get_bedding', methods=['GET'])
    def get_bedding():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row

        query = """
            SELECT
                b.bed_No AS bed_id,
                b.ward_No AS ward,
                CASE 
                    WHEN (
                        SELECT discharge_Date
                        FROM bedrecords br
                        WHERE br.bed_No = b.bed_No
                        ORDER BY br.admission_Date DESC
                        LIMIT 1
                    ) IS NULL
                    THEN 'Occupied'
                    ELSE 'Free'
                END AS status
            FROM bed b
            ORDER BY b.bed_No
            LIMIT 300;
        """

        df = pd.read_sql(query, conn)
        conn.close()
        return jsonify(df.to_dict(orient='records'))

    @app.route('/api/get_departments', methods=['GET'])
    def get_departments():
        query = """
            SELECT 
                dept_Id AS id,
                dept_Name AS name
            FROM department
            ORDER BY dept_Id
        """
        df = pd.read_sql(query, sqlite3.connect(DB_PATH))
        return jsonify(df.to_dict(orient='records'))

    @app.route('/api/get_nurses', methods=['GET'])
    def get_nurses():
        query = """
            SELECT
                nurse_Id AS id,
                FName || ' ' || LName AS name,
                COALESCE(conatct_No, '-') AS phone,
                Gender AS gender
            FROM nurse
            ORDER BY nurse_Id
        """
        df = pd.read_sql(query, sqlite3.connect(DB_PATH))
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

    @app.route('/api/get_helpers', methods=['GET'])
    def get_helpers():
        query = """
            SELECT
                helper_Id AS id,
                FName || ' ' || LName AS name,
                COALESCE(contact_No, '-') AS phone,
                Gender AS gender
            FROM helpers
            ORDER BY helper_Id
        """
        df = pd.read_sql(query, sqlite3.connect(DB_PATH))
        return jsonify(df.to_dict(orient='records'))

    @app.route('/api/get_doctors_list', methods=['GET'])
    def get_doctors_list():
        query = """
            SELECT
                doct_Id AS id,
                FName || ' ' || LName AS name,
                COALESCE(contact_No, '-') AS phone,
                Gender AS gender,
                surgeon_Type AS specialty
            FROM doctor
            ORDER BY doct_Id
        """
        df = pd.read_sql(query, sqlite3.connect(DB_PATH))
        return jsonify(df.to_dict(orient='records'))

    @app.route('/api/get_events', methods=['GET', 'POST'])
    def get_events():
        engine = create_engine(f"sqlite:///{DB_PATH}")
        query = """
            SELECT 
                a.appoIntment_Id AS id,

                p.FName || ' ' || p.LName AS patient_name,
                d.FName || ' ' || d.LName AS doctor_name,

                a.reason AS description,
                a.appointment_Date AS scheduled,

                -- FIX: Convert Booked → Scheduled
                CASE 
                    WHEN a.appointment_status = 'Booked' THEN 'Scheduled'
                    ELSE a.appointment_status
                END AS status

            FROM appointment a
            LEFT JOIN patients p 
                ON a.patient_Id = p.patient_Id
            LEFT JOIN doctor d
                ON a.doct_Id = d.doct_Id
            ORDER BY a.appointment_Date DESC
            LIMIT 100
        """
        try:
            df = pd.read_sql(query, engine).fillna("-")
            return jsonify(df.to_dict(orient='records'))
        except Exception as e:
            print("[ERROR] /api/get_events failed:", e)
            return jsonify([])



    @app.route('/api/get_patients', methods=['GET'])
    def get_patients():
        status = request.args.get("status", "admitted").lower()
        print(">>>> RUNNING PATIENT QUERY WITH STATUS =", status)
        DB_PATH_LOCAL = app.config["DB_PATH"]

        conn = sqlite3.connect(DB_PATH_LOCAL)
        conn.row_factory = sqlite3.Row

        query = f"""
            SELECT 
                p.patient_Id AS id,
                p.FName || ' ' || p.LName AS name,
                CASE 
                    WHEN p.email IS NULL 
                        OR p.email = '' 
                        OR LOWER(p.email) = 'unknown@example.com'
                    THEN LOWER(p.LName || '.' || p.FName || '@gmail.com')
                    ELSE p.email
                END AS email,
                p.contact_No AS phone,
                p.Gender AS gender,
                p.pt_Address AS address,
                CAST((julianday('now') - julianday(p.Date_Of_Birth)) / 365 AS INT) AS age,
                br.bed_No AS bed_number,
                br.admission_Date AS admitted_on,
                br.discharge_Date AS discharged_on,
                d.FName || ' ' || d.LName AS doctor
            FROM patients p
            LEFT JOIN bedrecords br 
                ON p.patient_Id = br.patient_Id
            LEFT JOIN staffshift s
                ON br.nurse_Id = s.nurse_Id
            LEFT JOIN doctor d
                ON s.doct_Id = d.doct_Id
            WHERE 1=1
        """

        if status == "admitted":
            query += " AND br.patient_Id IS NOT NULL AND br.discharge_Date IS NULL"
        elif status == "completed":
            query += " AND br.patient_Id IS NOT NULL AND br.discharge_Date IS NOT NULL"

        query += """
            GROUP BY p.patient_Id
            ORDER BY p.patient_Id DESC
            LIMIT 200
        """

        df = pd.read_sql(query, conn)
        conn.close()
        return jsonify(df.to_dict(orient="records"))

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
        # This is still here in case you manually emit bed_update from somewhere
        socketio.emit("bed_update_event", data)

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
