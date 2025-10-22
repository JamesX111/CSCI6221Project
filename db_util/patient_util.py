from datetime import datetime
from db_model import db, Patient
# ---------------------------------------------------
# Create a new patient
# ---------------------------------------------------
def create_patient(patient_data):
    """Create a new Patient record in the database."""
    required_fields = ['name', 'email', 'password']
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
def get_all_patients():
    """Retrieve all patients."""
    patients = Patient.query.all()
    return [p.to_dict() for p in patients] if hasattr(Patient, 'to_dict') else patients
