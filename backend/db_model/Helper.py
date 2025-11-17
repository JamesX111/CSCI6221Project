from . import db

class Helper(db.Model):
    """Helper table"""
    __tablename__ = 'helper'

    helper_Id = db.Column(db.Integer, primary_key=True)
    dept_Id = db.Column(db.Integer, db.ForeignKey('department.dept_Id'), nullable=False)

    FName = db.Column(db.String(100), nullable=False)
    LName = db.Column(db.String(100), nullable=False)

    Gender = db.Column(db.String(10), nullable=False)
    contact_No = db.Column(db.String(20), nullable=True)

    # Relationship to Department
    department = db.relationship("Department", backref="helpers", lazy=True)

    def __repr__(self):
        return f"<Helper {self.helper_Id} - {self.FName} {self.LName}>"

    def to_dict(self):
        return {
            "helper_Id": self.helper_Id,
            "dept_Id": self.dept_Id,
            "dept_Name": self.department.dept_Name if self.department else None,
            "FName": self.FName,
            "LName": self.LName,
            "Gender": self.Gender,
            "contact_No": self.contact_No,
        }
