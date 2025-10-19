from . import db
from datetime import datetime

class Event(db.Model):
    """Medical event or appointment model"""
    id = db.Column(db.Integer, primary_key=True)

    # Foreign keys
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    # Event metadata
    event_type = db.Column(db.String(50), nullable=False)  # e.g. 'Consultation', 'Surgery', 'Follow-up'
    description = db.Column(db.Text, nullable=True)
    scheduled_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    patient = db.relationship('Patient', backref='events', lazy=True)
    doctor = db.relationship('Doctor', backref='events', lazy=True)

    def __repr__(self):
        return f'<Event {self.event_type} on {self.scheduled_at} for Patient {self.patient_id}>'

    def to_dict(self):
        def format_datetime(dt):
            return dt.strftime('%Y-%m-%d %H:%M:%S') if dt else None

        return {
            'id': self.id,
            'event_type': self.event_type,
            'description': self.description,
            'scheduled_at': format_datetime(self.scheduled_at),
            'patient': {
                'id': self.patient.id,
                'name': self.patient.name
            } if self.patient else None,
            'doctor': {
                'id': self.doctor.id,
                'name': self.doctor.name,
                'department': self.doctor.department
            } if self.doctor else None
        }
