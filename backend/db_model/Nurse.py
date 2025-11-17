from . import db

class Nurse(db.Model):
    """Nurse table"""
    __tablename__ = 'nurse'

    nurse_Id = db.Column(db.Integer, primary_key=True)
    dept_Id = db.Column(db.Integer, nullable=False)

    FName = db.Column(db.String(100), nullable=False)
    LName = db.Column(db.String(100), nullable=False)

    Gender = db.Column(db.String(10), nullable=False)
    conatct_No = db.Column(db.String(20), nullable=True)  # Using your exact field name

    def __repr__(self):
        return f"<Nurse {self.nurse_Id} - {self.FName} {self.LName}>"

    def to_dict(self):
        return {
            "nurse_Id": self.nurse_Id,
            "dept_Id": self.dept_Id,
            "FName": self.FName,
            "LName": self.LName,
            "Gender": self.Gender,
            "conatct_No": self.conatct_No,
        }
