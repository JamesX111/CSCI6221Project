from datetime import datetime
from db_model import db, Patient
# ---------------------------------------------------
# Create a new patient
# ---------------------------------------------------
def create_patient(patient_data):
    """Create a new Patient record in the database."""
    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in patient_data or not patient_data[field]:
            raise ValueError(f"Missing required field: {field}")

    # Create new Patient instance
    new_patient = Patient(
        name=patient_data['name'],
        email=patient_data['email'],
        phone=patient_data.get('phone'),
        gender=patient_data.get('gender'),
        date_of_birth=patient_data.get('date_of_birth'),
        address=patient_data.get('address'),
        doctor_id=patient_data.get('doctor_id'),
    )

    # Use model’s password setter for hashing
    if 'password' in patient_data and patient_data['password']:
        new_patient.password = patient_data['password']

    # Save
    db.session.add(new_patient)
    db.session.commit()

    return new_patient.to_dict() if hasattr(new_patient, 'to_dict') else new_patient


# ---------------------------------------------------
# Update an existing patient
# ---------------------------------------------------
def update_patient(patient_id, update_data):
    """Update patient details by ID."""
    patient = Patient.query.get(patient_id)
    if not patient:
        raise ValueError(f"Patient with ID {patient_id} not found")

    for key, value in update_data.items():
        if key == 'password':
            patient.password = value
        elif hasattr(patient, key):
            setattr(patient, key, value)

    db.session.commit()
    return patient.to_dict() if hasattr(patient, 'to_dict') else patient


# ---------------------------------------------------
# Get a patient by ID **or** email
# ---------------------------------------------------
def get_patient(identifier):
    """
    Retrieve a patient by either ID (int) or email (str).
    Example:
        get_patient(1)
        get_patient("john@example.com")
    """
    if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
        # Treat as ID
        patient = Patient.query.get(int(identifier))
    elif isinstance(identifier, str):
        # Treat as email
        patient = Patient.query.filter_by(email=identifier).first()
    else:
        raise ValueError("Identifier must be an integer ID or a string email")

    if not patient:
        raise ValueError(f"Patient with identifier '{identifier}' not found")

    return patient.to_dict() if hasattr(patient, 'to_dict') else patient


# ---------------------------------------------------
# Get all patients
# ---------------------------------------------------
import sqlite3
import os

def get_all_patients():
    """Retrieve all patients directly from SQLite (readable DB)."""
    db_path = os.path.join(os.path.dirname(__file__), "../../data/hospital_raw.db")

    if not os.path.exists(db_path):
        print(f"[ERROR] Database not found at: {db_path}")
        return []

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
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    except Exception as e:
        print(f"[ERROR] Database query failed: {e}")
        return []

