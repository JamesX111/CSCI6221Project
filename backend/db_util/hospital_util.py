# create, update, delete and get hospital using table defined in db_model/hospital.py
from db_model import db, Hospital

def create_hospital(hospital_data):
    """
    Create a new Hospital record in the database.
    hospital_data should be a dict containing:
        - name (required)
        - address (optional)
        - phone (optional)
        - email (optional)
        - website (optional)
        - departments (optional dict with keys: emergency, pediatrics, cardiology, oncology,
          neurology, orthopedics, radiology, maternity)
    """

    # Validate required fields
    if 'name' not in hospital_data or not hospital_data['name']:
        raise ValueError("Missing required field: name")

    # Extract departments dict (default empty)
    departments = hospital_data.get('departments', {})

    new_hospital = Hospital(
        name=hospital_data['name'],
        address=hospital_data.get('address'),
        phone=hospital_data.get('phone'),
        email=hospital_data.get('email'),
        website=hospital_data.get('website'),
        has_emergency=departments.get('emergency', False),
        has_pediatrics=departments.get('pediatrics', False),
        has_cardiology=departments.get('cardiology', False),
        has_oncology=departments.get('oncology', False),
        has_neurology=departments.get('neurology', False),
        has_orthopedics=departments.get('orthopedics', False),
        has_radiology=departments.get('radiology', False),
        has_maternity=departments.get('maternity', False),
    )

    db.session.add(new_hospital)
    db.session.commit()

    return new_hospital.to_dict()



def get_hospital(hospital_id):
    hospital = Hospital.query.get(hospital_id)
    if not hospital:
        raise ValueError(f"Hospital with id {hospital_id} does not exist.")
    return hospital.to_dict()


def get_all_hospitals():
    hospitals = Hospital.query.all()
    return [hospital.to_dict() for hospital in hospitals]


def update_hospital(hospital_id, update_data):
    hospital = Hospital.query.get(hospital_id)
    if not hospital:
        raise ValueError(f"Hospital with id {hospital_id} does not exist.")

    # Update fields
    for key, value in update_data.items():
        if key == 'departments' and isinstance(value, dict):
            for dept_key, dept_value in value.items():
                attr_name = f"has_{dept_key}"
                if hasattr(hospital, attr_name):
                    setattr(hospital, attr_name, bool(dept_value))
                else:
                    raise ValueError(f"Invalid department field: {dept_key}")
        elif hasattr(hospital, key):
            setattr(hospital, key, value)
        else:
            raise ValueError(f"Invalid field: {key}")

    db.session.commit()
    return hospital.to_dict()


def delete_hospital(hospital_id):
    hospital = Hospital.query.get(hospital_id)
    if not hospital:
        raise ValueError(f"Hospital with id {hospital_id} does not exist.")

    db.session.delete(hospital)
    db.session.commit()
    return {"message": f"Hospital with id {hospital_id} has been deleted."}
