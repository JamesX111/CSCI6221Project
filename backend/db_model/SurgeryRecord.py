from . import db
from datetime import date, time

class SurgeryRecord(db.Model):
    """Surgery Record table"""
    __tablename__ = 'surgery_record'

    surgery_Id = db.Column(db.Integer, primary_key=True)

    patient_Id = db.Column(db.Integer, db.ForeignKey('patient.patient_Id'), nullable=False)
    surgeon_Id = db.Column(db.Integer, db.ForeignKey('doctor.doct_Id'), nullable=False)
    surgery_Type = db.Column(db.String(100), nullable=False)

    surgery_Date = db.Column(db.Date, nullable=False)
    start_Time = db.Column(db.Time, nullable=False)
    end_Time = db.Column(db.Time, nullable=False)

    room_no = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.String(500), nullable=True)

    nurse_Id = db.Column(db.Integer, db.ForeignKey('nurse.nurse_Id'), nullable=True)
    helper_Id = db.Column(db.Integer, db.ForeignKey('helper.helper_Id'), nullable=True)

    # Relationships
    patient = db.relationship("Patient", backref="surgeries", lazy=True)
    surgeon = db.relationship("Doctor", backref="surgeries", lazy=True)
    nurse = db.relationship("Nurse", backref="surgeries", lazy=True)
    helper = db.relationship("Helper", backref="surgeries", lazy=True)

    def __repr__(self):
        return f"<SurgeryRecord {self.surgery_Id} for Patient {self.patient_Id}>"

    def to_dict(self):
        return {
            "surgery_Id": self.surgery_Id,
            "patient_Id": self.patient_Id,
            "patient_Name": f"{self.patient.FName} {self.patient.LName}" if self.patient else None,
            "surgeon_Id": self.surgeon_Id,
            "surgeon_Name": f"{self.surgeon.FName} {self.surgeon.LName}" if self.surgeon else None,
            "surgery_Type": self.surgery_Type,
            "surgery_Date": self.surgery_Date.isoformat() if self.surgery_Date else None,
            "start_Time": self.start_Time.strftime("%H:%M:%S") if self.start_Time else None,
            "end_Time": self.end_Time.strftime("%H:%M:%S") if self.end_Time else None,
            "room_no": self.room_no,
            "notes": self.notes,
            "nurse_Id": self.nurse_Id,
            "nurse_Name": f"{self.nurse.FName} {self.nurse.LName}" if self.nurse else None,
            "helper_Id": self.helper_Id,
            "helper_Name": f"{self.helper.FName} {self.helper.LName}" if self.helper else None,
        }
