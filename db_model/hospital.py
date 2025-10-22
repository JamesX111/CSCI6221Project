from . import db

class Hospital(db.Model):
    """Hospital model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(100), nullable=True)

    # Department availability (stored as booleans: True/False)
    has_emergency = db.Column(db.Boolean, default=False, nullable=False)
    has_pediatrics = db.Column(db.Boolean, default=False, nullable=False)
    has_cardiology = db.Column(db.Boolean, default=False, nullable=False)
    has_oncology = db.Column(db.Boolean, default=False, nullable=False)
    has_neurology = db.Column(db.Boolean, default=False, nullable=False)
    has_orthopedics = db.Column(db.Boolean, default=False, nullable=False)
    has_radiology = db.Column(db.Boolean, default=False, nullable=False)
    has_maternity = db.Column(db.Boolean, default=False, nullable=False)

    # # Relationships (optional)
    # doctors = db.relationship('Doctor', backref='hospital', lazy=True)

    def __repr__(self):
        return f'<Hospital {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'website': self.website,
            'departments': {
                'emergency': self.has_emergency,
                'pediatrics': self.has_pediatrics,
                'cardiology': self.has_cardiology,
                'oncology': self.has_oncology,
                'neurology': self.has_neurology,
                'orthopedics': self.has_orthopedics,
                'radiology': self.has_radiology,
                'maternity': self.has_maternity,
            }
        }
