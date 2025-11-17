from . import db
from datetime import date, time

class StaffShift(db.Model):
    """Staff Shift table"""
    __tablename__ = 'staff_shift'

    shift_Id = db.Column(db.Integer, primary_key=True)

    doct_Id = db.Column(db.Integer, db.ForeignKey('doctor.doct_Id'), nullable=True)
    nurse_Id = db.Column(db.Integer, db.ForeignKey('nurse.nurse_Id'), nullable=True)
    helper_Id = db.Column(db.Integer, db.ForeignKey('helper.helper_Id'), nullable=True)

    shift_Date = db.Column(db.Date, nullable=False)
    shift_Start = db.Column(db.Time, nullable=False)
    shift_End = db.Column(db.Time, nullable=False)

    # Relationships
    doctor = db.relationship("Doctor", backref="shifts", lazy=True)
    nurse = db.relationship("Nurse", backref="shifts", lazy=True)
    helper = db.relationship("Helper", backref="shifts", lazy=True)

    def __repr__(self):
        return f"<StaffShift {self.shift_Id} on {self.shift_Date}>"

    def to_dict(self):
        return {
            "shift_Id": self.shift_Id,
            "doct_Id": self.doct_Id,
            "doctor_Name": f"{self.doctor.FName} {self.doctor.LName}" if self.doctor else None,
            "nurse_Id": self.nurse_Id,
            "nurse_Name": f"{self.nurse.FName} {self.nurse.LName}" if self.nurse else None,
            "helper_Id": self.helper_Id,
            "helper_Name": f"{self.helper.FName} {self.helper.LName}" if self.helper else None,
            "shift_Date": self.shift_Date.isoformat() if self.shift_Date else None,
            "shift_Start": self.shift_Start.strftime("%H:%M:%S") if self.shift_Start else None,
            "shift_End": self.shift_End.strftime("%H:%M:%S") if self.shift_End else None,
        }
