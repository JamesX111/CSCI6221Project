from . import db

class Appointment(db.Model):
    """Appointment model"""
    __tablename__ = 'appointment'
    appoIntment_Id = db.Column(db.Integer, primary_key=True)  # renamed PK

    # Foreign keys
    patient_Id = db.Column(db.Integer, db.ForeignKey('patient.patient_Id'), nullable=False)
    doct_Id = db.Column(db.Integer, db.ForeignKey('doctor.doct_Id'), nullable=False)

    # Appointment details
    reason = db.Column(db.String(255), nullable=True)
    appointment_Date = db.Column(db.DateTime, nullable=False)

    # Payment info
    payment_amount = db.Column(db.Float, nullable=True)
    mode_of_payment = db.Column(db.String(50), nullable=True)  # e.g., Cash, Insurance

    # Appointment metadata
    mode_of_appointment = db.Column(db.String(50), nullable=True)  # e.g., Online, In-person
    appointment_status = db.Column(db.String(20), nullable=False, default='Scheduled')  # e.g., Scheduled, Completed, Cancelled

    # Relationships
    patient = db.relationship('Patient', backref='appointments', lazy=True)
    doctor = db.relationship('Doctor', backref='appointments', lazy=True)

    def __repr__(self):
        return f'<Appointment {self.appoIntment_Id} on {self.appointment_Date} for Patient {self.patient_Id}>'

    def to_dict(self):
        def format_datetime(dt):
            return dt.strftime('%Y-%m-%d %H:%M:%S') if dt else None

        return {
            'appoIntment_Id': self.appoIntment_Id,
            'appointment_Date': format_datetime(self.appointment_Date),
            'reason': self.reason,
            'appointment_status': self.appointment_status,
            'payment_amount': self.payment_amount,
            'mode_of_payment': self.mode_of_payment,
            'mode_of_appointment': self.mode_of_appointment,
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
