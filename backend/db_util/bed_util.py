# create, update, delete and get bed occupancy using table defined in db_model/bed_occupancy.py
from db_model import db, BedOccupancy

def create_bed(bed_data):
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
    bed = BedOccupancy.query.get(bed_id)
    if not bed:
        raise ValueError(f"Bed with id {bed_id} does not exist.")
    return bed.to_dict()


def get_all_beds():
    beds = BedOccupancy.query.all()
    return [bed.to_dict() for bed in beds]


def get_beds_by_status_and_hospital(status, hospital_id):
    if not status:
        raise ValueError("Status must be provided.")
    if not hospital_id:
        raise ValueError("Hospital ID must be provided.")
    beds = BedOccupancy.query.filter_by(status=status, hospital_id=hospital_id).all()
    return [bed.to_dict() for bed in beds]


def update_bed(bed_id, update_data):
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
    bed = BedOccupancy.query.get(bed_id)
    if not bed:
        raise ValueError(f"Bed with id {bed_id} does not exist.")

    db.session.delete(bed)
    db.session.commit()
    return {"message": f"Bed with id {bed_id} has been deleted."}
