from . import db
from datetime import datetime

class BedOccupancy(db.Model):
    """Bed Occupancy model"""
    __tablename__ = 'bed_occupancy'


    bed_id = db.Column(db.Integer, primary_key=True)
    ward = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=True)
    hospital = db.relationship('Hospital', backref='beds', lazy=True)

    def __repr__(self):
        return f'<BedOccupancy bed_id={self.bed_id}, ward={self.ward}, status={self.status}>'

    def to_dict(self):
        return {
            'bed_id': self.bed_id,
            'ward': self.ward,
            'status': self.status,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'hospital_id': self.hospital_id
        }
