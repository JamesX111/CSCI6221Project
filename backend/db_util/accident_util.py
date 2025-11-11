from db_model import db, Accident
from datetime import datetime

def get_all_accidents():
    """Return all accidents."""
    accidents = Accident.query.all()
    return [a.to_dict() for a in accidents]

def get_accident_by_id(accident_id):
    """Return a single accident by ID."""
    accident = Accident.query.get(accident_id)
    if not accident:
        raise ValueError(f"Accident with ID {accident_id} not found.")
    return accident.to_dict()

def create_accident(data):
    """Create a new accident record."""
    try:
        occurred_at = data.get('occurred_at')
        if occurred_at:
            # Parse datetime-local format (YYYY-MM-DDTHH:MM)
            occurred_at = datetime.fromisoformat(occurred_at)
        else:
            occurred_at = datetime.utcnow()

        accident = Accident(
            patient_id=data.get('patient_id'),
            location=data['location'],
            accident_type=data['accident_type'],
            description=data.get('description'),
            occurred_at=occurred_at,
            severity=data.get('severity', 'Low')  # Default = Low
        )
        db.session.add(accident)
        db.session.commit()
        return accident
    except KeyError as e:
        raise ValueError(f"Missing required field: {str(e)}")
    except Exception as e:
        db.session.rollback()
        raise e

def update_accident(accident_id, data):
    """Update an existing accident record."""
    accident = Accident.query.get(accident_id)
    if not accident:
        raise ValueError(f"Accident with ID {accident_id} not found.")

    # Update fields if present
    accident.accident_type = data.get('accident_type', accident.accident_type)
    accident.description = data.get('description', accident.description)
    accident.location = data.get('location', accident.location)
    accident.severity = data.get('severity', accident.severity)
    accident.patient_id = data.get('patient_id', accident.patient_id)

    if 'occurred_at' in data and data['occurred_at']:
        accident.occurred_at = datetime.fromisoformat(data['occurred_at'])

    db.session.commit()
    return accident.to_dict()

def delete_accident(accident_id):
    """Delete an accident record."""
    accident = Accident.query.get(accident_id)
    if not accident:
        raise ValueError(f"Accident with ID {accident_id} not found.")
    db.session.delete(accident)
    db.session.commit()
    return {"message": f"Accident with ID {accident_id} deleted successfully."}
