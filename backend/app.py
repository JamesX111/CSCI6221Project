# ===============================================================
# Hospital Management Backend (Updated for Normalized Database)
# ===============================================================
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import sqlite3
import pandas as pd
import sys, os
from flask_socketio import SocketIO, emit
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# ---------------------------------------------------------------
# 1. Application and Database Configuration
# ---------------------------------------------------------------
app = Flask(__name__)

# Absolute path to the normalized database
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/hospital_raw.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
# CORS(app, resources={"/*": {"origins": "*"}})
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
@socketio.on("bed_update")
def handle_bed_update(data):
    # Broadcast to all connected clients
    emit("bed_update_event", data, broadcast=True)


# Utility function to query tables directly with pandas
def read_table(query):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print(f"[ERROR] Database query failed: {e}")
        return pd.DataFrame()


# ---------------------------------------------------------------
# 2. API ROUTES (Updated to Match Normalized Schema)
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# /api/get_hospitals – Retrieves all departments or hospital info
# ---------------------------------------------------------------
@app.route('/api/get_hospitals', methods=['GET', 'POST'])
def get_hospitals():
    import pandas as pd
    from sqlalchemy import create_engine
    import os

    db_path = os.path.join(os.path.dirname(__file__), '../data/hospital_raw.db')
    engine = create_engine(f'sqlite:///{db_path}')

    query = """
        SELECT 
            dept_Id AS id,
            dept_Name AS name,
            '-' AS address,
            '-' AS phone,
            '-' AS email,
            '-' AS departments
        FROM department
        LIMIT 50
    """

    df = pd.read_sql(query, engine)
    return jsonify(df.to_dict(orient='records'))



# ---------------------------------------------------------------
# /api/get_doctors – Retrieve doctors by department (if available)
# ---------------------------------------------------------------
@app.route("/api/get_doctors", methods=["GET", "POST"])
def get_doctors():
    data = request.get_json()
    department = data.get("department", None)

    if department:
        query = f"""
            SELECT DISTINCT staff_name AS doctor_name, role, shift_start, shift_end
            FROM staff_schedule
            WHERE role LIKE '%Doctor%' OR role LIKE '%Physician%'
            LIMIT 50
        """
    else:
        query = """
            SELECT DISTINCT staff_name AS doctor_name, role, shift_start, shift_end
            FROM staff_schedule
            LIMIT 50
        """

    df = read_table(query)
    return jsonify(df.to_dict(orient="records"))


# ---------------------------------------------------------------
# /api/get_bedding – Retrieve current bed occupancy and status
# ---------------------------------------------------------------
@app.route('/api/get_bedding', methods=['GET', 'POST'])
def get_bedding():
    import pandas as pd
    from sqlalchemy import create_engine
    import os

    db_path = os.path.join(os.path.dirname(__file__), '../data/hospital_raw.db')
    engine = create_engine(f'sqlite:///{db_path}')

    query = """
        SELECT 
            bed_No AS bed_id,
            ward_No AS ward,
            '-' AS status,
            '-' AS last_updated
        FROM bed
        LIMIT 100
    """

    df = pd.read_sql(query, engine)
    return jsonify(df.to_dict(orient='records'))




# ---------------------------------------------------------------
# /api/get_events – Retrieve appointments or admissions timeline
# ---------------------------------------------------------------
@app.route('/api/get_events', methods=['GET', 'POST'])
def get_events():
    """
    Retrieves appointment data from the normalized hospital database
    and maps it to the frontend event schema.
    """

    import pandas as pd
    from sqlalchemy import create_engine
    import os

    db_path = os.path.join(os.path.dirname(__file__), '../data/hospital_raw.db')
    engine = create_engine(f'sqlite:///{db_path}')

    query = """
        SELECT 
            appoIntment_Id AS id,
            patient_Id AS patient,
            doct_Id AS doctor,
            reason AS description,
            appointment_Date AS scheduled,
            appointment_status AS status,
            mode_of_appointment AS type
        FROM appointment
        LIMIT 100
    """

    try:
        df = pd.read_sql(query, engine)
 
        # Ensure all columns exist and fill NaN with "-"
        for col in ["id", "type", "description", "scheduled", "status", "doctor", "patient"]:
            if col not in df.columns:
                df[col] = "-"
        df = df.fillna("-")

        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        print(f"[ERROR] /api/get_events failed: {e}")
        return jsonify([])




@app.route('/api/get_patients', methods=['GET', 'POST'])
def get_patients():
    import pandas as pd
    from sqlalchemy import create_engine
    import os

    db_path = os.path.join(os.path.dirname(__file__), '../data/hospital_raw.db')
    engine = create_engine(f'sqlite:///{db_path}')

    query = """
        SELECT 
            patient_Id AS id,
            FName || ' ' || LName AS name,
            email,
            contact_No AS phone,
            Gender AS gender,
            pt_Address AS address
        FROM patients
        LIMIT 100
    """

    try:
        df = pd.read_sql(query, engine)
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)})


# ---------------------------------------------------------------
# /api/forecast – Integrate ARIMA inflow prediction
# ---------------------------------------------------------------
@app.route("/api/forecast", methods=["GET"])
def forecast_inflow():
    from implementation import forecast_inflow
    forecast_df = forecast_inflow(days_ahead=7)
    return jsonify(forecast_df.to_dict(orient="records"))

@app.route("/api/forecast_summary", methods=["GET"])
def forecast_summary():
    try:
        from implementation import forecast_inflow, generate_ai_summary

        # Read horizon parameter (default = 7)
        horizon = request.args.get("days", default=7, type=int)

        # Validate allowed values
        if horizon not in [3, 7, 14, 30]:
            horizon = 7

        forecast_df = forecast_inflow(days_ahead=horizon)

        if forecast_df.empty:
            return jsonify({
                "forecast": [],
                "summary": "No forecast available (empty bedrecords table)."
            })

        summary = generate_ai_summary(forecast_df)

        return jsonify({
            "forecast": forecast_df.to_dict(orient="records"),
            "summary": summary,
            "horizon": horizon
        })

    except Exception as e:
        print(f"[ERROR] /api/forecast_summary failed: {e}")
        return jsonify({
            "error": str(e),
            "forecast": [],
            "summary": "Error generating summary."
        })

# ---------------------------------------------------------------
# Root route (for testing)
# ---------------------------------------------------------------
@app.route("/")
def index():
    return jsonify({"message": "Hospital Management Backend is running with normalized DB."})


# ---------------------------------------------------------------
# Run Application
# ---------------------------------------------------------------
if __name__ == "__main__":
    print(f"Using database at: {DB_PATH}")
    app.run(debug=True, port=5000)
