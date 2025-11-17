from . import db
from datetime import datetime

class MedicalRecord(db.Model):
    """Medical Record table"""
    __tablename__ = 'medical_record'

    record_Id = db.Column(db.Integer, primary_key=True)

    doct_Id = db.Column(db.Integer, db.ForeignKey('doctor.doct_Id'), nullable=False)
    patient_Id = db.Column(db.Integer, db.ForeignKey('patient.patient_Id'), nullable=False)

    visit_Date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    curr_Weight = db.Column(db.Float, nullable=True)
    curr_height = db.Column(db.Float, nullable=True)
    curr_Blood_Pressure = db.Column(db.String(20), nullable=True)
    curr_Temp_F = db.Column(db.Float, nullable=True)

    diagnosis = db.Column(db.String(500), nullable=True)
    treatment = db.Column(db.String(500), nullable=True)

    next_Visit = db.Column(db.DateTime, nullable=True)

    # Relationships
    doctor = db.relationship("Doctor", backref="medical_records", lazy=True)
    patient = db.relationship("Patient", backref="medical_records", lazy=True)

    def __repr__(self):
        return f"<MedicalRecord {self.record_Id} for Patient {self.patient_Id}>"

    def to_dict(self):
        return {
            "record_Id": self.record_Id,
            "doct_Id": self.doct_Id,
            "doctor_Name": f"{self.doctor.FName} {self.doctor.LName}" if self.doctor else None,
            "patient_Id": self.patient_Id,
            "patient_Name": f"{self.patient.FName} {self.patient.LName}" if self.patient else None,
            "visit_Date": self.visit_Date.isoformat() if self.visit_Date else None,
            "curr_Weight": self.curr_Weight,
            "curr_height": self.curr_height,
            "curr_Blood_Pressure": self.curr_Blood_Pressure,
            "curr_Temp_F": self.curr_Temp_F,
            "diagnosis": self.diagnosis,
            "treatment": self.treatment,
            "next_Visit": self.next_Visit.isoformat() if self.next_Visit else None,
        }
