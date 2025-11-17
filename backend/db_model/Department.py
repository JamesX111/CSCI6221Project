from . import db

class Department(db.Model):
    """Department model"""
    __tablename__ = 'department'

    dept_Id = db.Column(db.Integer, primary_key=True)
    dept_Name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Department {self.dept_Id} - {self.dept_Name}>"

    def to_dict(self):
        return {
            "dept_Id": self.dept_Id,
            "dept_Name": self.dept_Name,
        }