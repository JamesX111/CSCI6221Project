from . import db

class Room(db.Model):
    """Room table"""
    __tablename__ = 'room'

    room_No = db.Column(db.Integer, primary_key=True)
    dept_Id = db.Column(db.Integer, db.ForeignKey('department.dept_Id'), nullable=False)
    room_Type = db.Column(db.String(100), nullable=False)

    # Relationship to Department
    department = db.relationship("Department", backref="rooms", lazy=True)

    def __repr__(self):
        return f"<Room {self.room_No} - {self.room_Type}>"

    def to_dict(self):
        return {
            "room_No": self.room_No,
            "dept_Id": self.dept_Id,
            "department_Name": self.department.dept_Name if self.department else None,
            "room_Type": self.room_Type,
        }
