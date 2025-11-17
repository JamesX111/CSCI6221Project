# create, update, delete and get doctor using table defined in db_model/doctor.py
# from backend.db_model import db



def create_doctor(doctor_data):
    from backend.db_model import db
    from backend.db_model.doctor import Doctor
    from backend.db_model.hospital import Hospital
    if 'name' not in doctor_data or not doctor_data['name']:
        raise ValueError("Missing required field: name")
    if 'department' not in doctor_data or not doctor_data['department']:
        raise ValueError("Missing required field: department")

    hospital = None
    if 'hospital_id' in doctor_data and doctor_data['hospital_id'] is not None:
        hospital = Hospital.query.get(doctor_data['hospital_id'])
        if not hospital:
            raise ValueError(f"Hospital with id {doctor_data['hospital_id']} does not exist.")

    new_doctor = Doctor(
        name=doctor_data['name'],
        email=doctor_data.get('email'),
        phone=doctor_data.get('phone'),
        specialty=doctor_data.get('specialty'),
        department=doctor_data['department'],
        hospital=hospital
    )

    db.session.add(new_doctor)
    db.session.commit()
    return new_doctor.to_dict() if hasattr(new_doctor, "to_dict") else new_doctor


def get_doctor(doctor_id):
    from backend.db_model import db
    from backend.db_model.doctor import Doctor
    from backend.db_model.hospital import Hospital
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        raise ValueError(f"Doctor with id {doctor_id} does not exist.")
    return doctor.to_dict()


def get_all_doctors():
    from backend.db_model import db
    from backend.db_model.doctor import Doctor
    from backend.db_model.hospital import Hospital
    doctors = Doctor.query.all()
    return [doctor.to_dict() for doctor in doctors]


def get_doctors_by_hospital(hospital_id):
    from backend.db_model import db
    from backend.db_model.doctor import Doctor
    from backend.db_model.hospital import Hospital
    hospital = Hospital.query.get(hospital_id)
    if not hospital:
        raise ValueError(f"Hospital with id {hospital_id} does not exist.")
    doctors = Doctor.query.filter_by(hospital_id=hospital_id).all()
    return [doctor.to_dict() for doctor in doctors]


def get_doctors_by_department(department):
    from backend.db_model import db
    from backend.db_model.doctor import Doctor
    from backend.db_model.hospital import Hospital
    if not department:
        raise ValueError("Department must be provided.")
    doctors = Doctor.query.filter_by(department=department).all()
    return [doctor.to_dict() for doctor in doctors]


def update_doctor(doctor_id, update_data):
    from backend.db_model import db
    from backend.db_model.doctor import Doctor
    from backend.db_model.hospital import Hospital
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        raise ValueError(f"Doctor with id {doctor_id} does not exist.")

    for key, value in update_data.items():
        if key == 'hospital_id':
            if value is None:
                doctor.hospital = None
            else:
                hospital = Hospital.query.get(value)
                if not hospital:
                    raise ValueError(f"Hospital with id {value} does not exist.")
                doctor.hospital = hospital
        elif hasattr(doctor, key):
            setattr(doctor, key, value)
        else:
            raise ValueError(f"Invalid field: {key}")

    db.session.commit()
    return doctor.to_dict()


def delete_doctor(doctor_id):
    from backend.db_model import db
    from backend.db_model.doctor import Doctor
    from backend.db_model.hospital import Hospital
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        raise ValueError(f"Doctor with id {doctor_id} does not exist.")

    db.session.delete(doctor)
    db.session.commit()
    return {"message": f"Doctor with id {doctor_id} has been deleted."}
