from . import db

class Bed(db.Model):
    """Hospital Bed model"""
    __tablename__ = 'bed'
    bed_No = db.Column(db.Integer, primary_key=True)  # Primary key: bed number
    ward_No = db.Column(db.Integer, nullable=False)  # Ward identifier

    # Optional: add a relationship to Ward model if you have one
    # ward = db.relationship('Ward', backref='beds', lazy=True)

    def __repr__(self):
        return f"<Bed {self.bed_No} in Ward {self.ward_No}>"

    def to_dict(self):
        return {
            'bed_No': self.bed_No,
            'ward_No': self.ward_No
        }
