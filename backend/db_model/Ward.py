from . import db

class Ward(db.Model):
    """Ward table"""
    __tablename__ = 'ward'

    ward_No = db.Column(db.Integer, primary_key=True)
    ward_Name = db.Column(db.String(100), nullable=False)
    dept_Id = db.Column(db.Integer, db.ForeignKey('department.dept_Id'), nullable=False)

    # Relationship to Department
    department = db.relationship("Department", backref="wards", lazy=True)

    def __repr__(self):
        return f"<Ward {self.ward_No} - {self.ward_Name}>"

    def to_dict(self):
        return {
            "ward_No": self.ward_No,
            "ward_Name": self.ward_Name,
            "dept_Id": self.dept_Id,
            "dept_Name": self.department.dept_Name if self.department else None
        }
