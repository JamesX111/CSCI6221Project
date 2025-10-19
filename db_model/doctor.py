from . import db

class Doctor(db.Model):
    """Doctor model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    specialty = db.Column(db.String(100), nullable=True)

    # Department is a string, not a relationship
    department = db.Column(db.String(50), nullable=False)  # e.g., 'Cardiology', 'Emergency'

    # Hospital relationship
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=True)
    hospital = db.relationship('Hospital', backref='doctors', lazy=True)

    def __repr__(self):
        return f'<Doctor {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'specialty': self.specialty,
            'department': self.department,
            'hospital': {
                'id': self.hospital.id,
                'name': self.hospital.name
            } if self.hospital else None
        }
