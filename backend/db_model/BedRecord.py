from . import db
from datetime import datetime

class BedRecord(db.Model):
    """Bed Record model"""
    __tablename__ = 'bed_record'

    admission_Id = db.Column(db.Integer, primary_key=True)
    bed_No = db.Column(db.Integer, db.ForeignKey('bed.bed_No'), nullable=False)
    patient_Id = db.Column(db.Integer, db.ForeignKey('patient.patient_Id'), nullable=False)
    nurse_Id = db.Column(db.Integer, db.ForeignKey('nurse.nurse_Id'), nullable=True)
    helper_Id = db.Column(db.Integer, db.ForeignKey('helper.helper_Id'), nullable=True)

    admission_Date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    discharge_Date = db.Column(db.DateTime, nullable=True)

    amount = db.Column(db.Float, nullable=True)
    mode_of_payment = db.Column(db.String(50), nullable=True)

    # Relationships
    bed = db.relationship("Bed", backref="bed_records", lazy=True)
    patient = db.relationship("Patient", backref="bed_records", lazy=True)
    nurse = db.relationship("Nurse", backref="bed_records", lazy=True)
    helper = db.relationship("Helper", backref="bed_records", lazy=True)

    def __repr__(self):
        return f"<BedRecord {self.admission_Id} - Bed {self.bed_No}>"

    def to_dict(self):
        return {
            "admission_Id": self.admission_Id,
            "bed_No": self.bed_No,
            "patient_Id": self.patient_Id,
            "patient_Name": f"{self.patient.FName} {self.patient.LName}" if self.patient else None,
            "nurse_Id": self.nurse_Id,
            "nurse_Name": f"{self.nurse.FName} {self.nurse.LName}" if self.nurse else None,
            "helper_Id": self.helper_Id,
            "helper_Name": f"{self.helper.FName} {self.helper.LName}" if self.helper else None,
            "admission_Date": self.admission_Date.isoformat() if self.admission_Date else None,
            "discharge_Date": self.discharge_Date.isoformat() if self.discharge_Date else None,
            "amount": self.amount,
            "mode_of_payment": self.mode_of_payment,
        }
