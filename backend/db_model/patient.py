from . import db
from datetime import date

class Patient(db.Model):
    """Patient table"""
    __tablename__ = 'patient'

    patient_Id = db.Column(db.Integer, primary_key=True)

    FName = db.Column(db.String(100), nullable=False)
    LName = db.Column(db.String(100), nullable=False)

    Gender = db.Column(db.String(10), nullable=False)

    Date_Of_Birth = db.Column(db.Date, nullable=False)

    contact_No = db.Column(db.String(20), nullable=True)
    pt_Address = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Patient {self.patient_Id} - {self.FName} {self.LName}>"

    def to_dict(self):
        return {
            "patient_Id": self.patient_Id,
            "FName": self.FName,
            "LName": self.LName,
            "Gender": self.Gender,
            "Date_Of_Birth": self.Date_Of_Birth.isoformat() if self.Date_Of_Birth else None,
            "contact_No": self.contact_No,
            "pt_Address": self.pt_Address,
        }
