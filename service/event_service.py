# create, update, delete and get event using table defined in db_models/event.py
from db_model import db, Event
from flask_sqlalchemy import SQLAlchemy



def create_event(event_data):
    # Validate input data
    required_fields = ['name', 'date', 'location']
    for field in required_fields:
        if field not in event_data:
            raise ValueError(f"Missing required field: {field}")

    # Create new Event instance
    new_event = Event(
        name=event_data['name'],
        date=event_data['date'],
        location=event_data['location'],
        description=event_data.get('description')  # Optional field
    )

    # Add to session and commit
    db.add(new_event)
    db.commit()

    return new_event.to_dict()

def get_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        raise ValueError(f"Event with id {event_id} does not exist.")
    return event.to_dict()

def update_event(event_id, update_data):
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
    event = Event.query.get(event_id)
    if not event:
        raise ValueError(f"Event with id {event_id} does not exist.")

    db.delete(event)
    db.commit()
    return {"message": f"Event with id {event_id} has been deleted."}