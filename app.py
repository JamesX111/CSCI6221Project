from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db_model import db, init_db
app = Flask(__name__)

from flask import Flask
from db_model import init_db, db, Patient

def create_app():
    app = Flask(__name__)

    # Configure the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database
    init_db(app)

    return app

def reset_db(app):
    """Completely reset the database (drop all tables, then recreate)."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("✅ Database has been reset!")


def test_db():
    with app.app_context():
    # Create a new patient instance
        new_patient = Patient(
            name='John Doe',
            email='john.doe@example.com',
            phone='1234567890',
            gender='male',
            address='123 Main Street',
        )

        # Set password (uses your setter method)
        new_patient.password = 'secret123'

        # Add to session and commit
        db.session.add(new_patient)
        db.session.commit()

app = create_app()

@app.route('/')
def index():
    # test_db()
    patient = Patient.query.filter_by(email='john.doe@example.com').first()
    print("🔍 Patient as dict:", patient.to_dict())
    return "Database initialized and app running!"

if __name__ == '__main__':
    app.run(debug=True)



