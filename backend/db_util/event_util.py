# create, update, delete and get event using table defined in db_models/event.py
# from backend.db_model import db

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

def create_event(event_data):
    from backend.db_model import db
    from backend.db_model.event import Event
    """
    Create a new Event record in the database.
    event_data should be a dict containing:
        - patient_id (required)
        - doctor_id (required)
        - event_type (required)
        - description (optional)
        - scheduled_at (optional, defaults to now)
        - payment_amount (optional)
        - payment_method (optional)
        - status (optional, defaults to 'Scheduled')
    """

    # Validate required fields
    required_fields = ['patient_id', 'doctor_id', 'event_type']
    for field in required_fields:
        if field not in event_data or event_data[field] is None:
            raise ValueError(f"Missing required field: {field}")

    # Create a new Event instance
    new_event = Event(
        patient_id = event_data['patient_id'],
        doctor_id = event_data['doctor_id'],
        event_type = event_data['event_type'],
        description = event_data.get('description'),
        scheduled_at = event_data.get('scheduled_at', datetime.utcnow()),
        payment_amount = event_data.get('payment_amount'),
        payment_method = event_data.get('payment_method'),
        status = event_data.get('status', 'Initialized'),
    )

    # Add to session and commit
    db.session.add(new_event)
    db.session.commit()

    return new_event.to_dict() if hasattr(new_event, "to_dict") else new_event


def get_event(event_id):
    from backend.db_model import db
    from backend.db_model.event import Event
    event = Event.query.get(event_id)
    if not event:
        raise ValueError(f"Event with id {event_id} does not exist.")
    return event.to_dict()

def update_event(event_id, update_data):
    from backend.db_model import db
    from backend.db_model.event import Event
    event = Event.query.get(event_id)
    if not event:
        raise ValueError(f"Event with id {event_id} does not exist.")

    # Update fields
    for key, value in update_data.items():
        if hasattr(event, key):
            setattr(event, key, value)
        else:
            raise ValueError(f"Invalid field: {key}")

    db.commit()
    return event.to_dict()

def delete_event(event_id):
    from backend.db_model import db
    from backend.db_model.event import Event
    event = Event.query.get(event_id)
    if not event:
        raise ValueError(f"Event with id {event_id} does not exist.")

    db.delete(event)
    db.commit()
    return {"message": f"Event with id {event_id} has been deleted."}

def get_all_events():
    from backend.db_model import db, Event
    events = Event.query.all()
    return [event.to_dict() for event in events] if hasattr(Event, "to_dict") else events
