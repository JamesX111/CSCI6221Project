from . import db
import secrets
from werkzeug.security import generate_password_hash, check_password_hash

class Patient(db.Model):
    """Patient model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    gender = db.Column(db.String(10))  # 'male', 'female', 'other'
    date_of_birth = db.Column(db.Date, nullable=True)
    address = db.Column(db.String(255), nullable=True)

    # Password fields
    password_hash = db.Column(db.String(255), nullable=True)
    password_salt = db.Column(db.String(32), nullable=True)

    # Relationship to doctor
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=True)
    doctor = db.relationship('Doctor', backref='patients', lazy=True)

    @property
    def password(self):
        # Prevent direct access to password
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        # Generate salt and hashed password
        self.password_salt = secrets.token_hex(16)
        self.password_hash = generate_password_hash(f"{password}{self.password_salt}")

    def verify_password(self, password):
        # Check if the provided password matches the stored hash
        return check_password_hash(self.password_hash, f"{password}{self.password_salt}")

    def __repr__(self):
        return f'<Patient {self.name}>'

    def to_dict(self):
        # Format date of birth for JSON output
        def format_date(d):
            return d.strftime('%Y-%m-%d') if d else None

        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'gender': self.gender,
            'date_of_birth': format_date(self.date_of_birth),
            'address': self.address,
            'doctor': {
                'id': self.doctor.id,
                'name': self.doctor.name
            } if self.doctor else None
        }
