from . import db
from datetime import datetime

class Accident(db.Model):
    """Accident report model"""
    id = db.Column(db.Integer, primary_key=True)

    # Foreign keys
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=True)
    location = db.Column(db.String(100), nullable=False)  # e.g. 'Room 101', 'Building A'

    # Accident metadata
    accident_type = db.Column(db.String(50), nullable=False)  # e.g. 'Fall', 'Collision', 'Burn'
    description = db.Column(db.Text, nullable=True)
    occurred_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    severity = db.Column(db.String(20), nullable=False, default='Low')  # Default severity

    # Relationships
    patient = db.relationship('Patient', backref='accidents', lazy=True)

    def __repr__(self):
        return f'<Accident {self.accident_type} on {self.occurred_at} for Patient {self.patient_id}>'

    def to_dict(self):
        def format_datetime(dt):
            return dt.strftime('%Y-%m-%d %H:%M:%S') if dt else None

        return {
            'id': self.id,
            'accident_type': self.accident_type,
            'description': self.description,
            'occurred_at': format_datetime(self.occurred_at),
            'severity': self.severity,
            'location': self.location,
            'patient': {
                'id': self.patient.id,
                'name': self.patient.name
            } if self.patient else None
        }
