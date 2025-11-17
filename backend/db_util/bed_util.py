# create, update, delete and get bed occupancy using table defined in db_model/bed_occupancy.py
# from backend.db_model import db
# from backend.app import db
# from backend.db_model.bed_occupancy import BedOccupancy


def create_bed(bed_data):
    from backend.db_model import db
    from backend.db_model.bed_occupancy import BedOccupancy
    """
    Create a new BedOccupancy record in the database.
    bed_data should be a dict containing:
        - ward (optional)
        - status (optional, default 'Available')
        - hospital_id (optional)
    """
    new_bed = BedOccupancy(
        ward=bed_data.get('ward'),
        status=bed_data.get('status', 'Available'),
        hospital_id=bed_data.get('hospital_id')
    )

    db.session.add(new_bed)
    db.session.commit()

    return new_bed.to_dict() if hasattr(new_bed, "to_dict") else new_bed


def get_bed(bed_id):
    from backend.db_model import db
    from backend.db_model.bed_occupancy import BedOccupancy
    bed = BedOccupancy.query.get(bed_id)
    if not bed:
        raise ValueError(f"Bed with id {bed_id} does not exist.")
    return bed.to_dict()


def get_all_beds():
    from backend.db_model import db
    from backend.db_model.bed_occupancy import BedOccupancy
    beds = BedOccupancy.query.all()
    return [bed.to_dict() for bed in beds]


def get_beds_by_status_and_hospital(status, hospital_id):
    from backend.db_model import db
    from backend.db_model.bed_occupancy import BedOccupancy
    if not status:
        raise ValueError("Status must be provided.")
    if not hospital_id:
        raise ValueError("Hospital ID must be provided.")
    beds = BedOccupancy.query.filter_by(status=status, hospital_id=hospital_id).all()
    return [bed.to_dict() for bed in beds]


def update_bed(bed_id, update_data):
    from backend.db_model import db
    from backend.db_model.bed_occupancy import BedOccupancy
    bed = BedOccupancy.query.get(bed_id)
    if not bed:
        raise ValueError(f"Bed with id {bed_id} does not exist.")

    for key, value in update_data.items():
        if hasattr(bed, key):
            setattr(bed, key, value)
        else:
            raise ValueError(f"Invalid field: {key}")

    db.session.commit()
    return bed.to_dict()


def delete_bed(bed_id):
    from backend.app import db
    from backend.db_model.bed_occupancy import BedOccupancy
    bed = BedOccupancy.query.get(bed_id)
    if not bed:
        raise ValueError(f"Bed with id {bed_id} does not exist.")

    db.session.delete(bed)
    db.session.commit()
    return {"message": f"Bed with id {bed_id} has been deleted."}


# ===============================================================
# Simulation-only function: Allocate bed from normalized database
# ===============================================================
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../../data/hospital_raw.db")

def allocate_available_bed():
    """
    Returns the first available bed_No (does NOT insert).
    A bed is available if it has no active bedrecords entry.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
        SELECT bed_No
        FROM bed
        WHERE bed_No NOT IN (
            SELECT bed_No FROM bedrecords WHERE discharge_Date IS NULL
        )
        LIMIT 1;
    """

    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return row[0]


def assign_patient_to_bed(patient_id, bed_no):
    """
    Assign a patient to a specific bed by inserting a new bedrecords row.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if bed is already occupied
    cursor.execute("""
        SELECT 1 FROM bedrecords
        WHERE bed_No = ? AND discharge_Date IS NULL
    """, (bed_no,))
    
    if cursor.fetchone():
        conn.close()
        raise ValueError(f"Bed {bed_no} is already occupied.")

    # Insert new admission record
    cursor.execute("""
        INSERT INTO bedrecords (
            bed_No, patient_Id, nurse_Id, helper_Id,
            admission_Date, discharge_Date, amount, mode_of_payment
        )
        VALUES (?, ?, NULL, NULL, datetime('now'), NULL, NULL, NULL)
    """, (bed_no, patient_id))

    conn.commit()
    conn.close()

    return True
