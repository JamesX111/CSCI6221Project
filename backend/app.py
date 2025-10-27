from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from db_model import db, init_db
from flask_cors import CORS
app = Flask(__name__)


from flask import Flask
from db_model import init_db, db, Patient, Doctor, Hospital, Event, BedOccupancy

def create_app():
    app = Flask(__name__)

    # Configure the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database
    init_db(app)

    return app

app = create_app()
CORS(app)

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



# Routes

@app.route('/api/reset_db', methods=['POST'])
def reset_database_route():
    reset_db(app)
    return jsonify({"message": "Database has been reset!"})

# get all patients
@app.route('/api/get_patients', methods=['POST'])
def get_patients():
    with app.app_context():
        patients = Patient.query.all()
        patients_list = [patient.to_dict() for patient in patients]
        return jsonify(patients_list)

# get all hospitals
@app.route('/api/get_hospitals', methods=['POST'])
def get_hospitals():
    from db_model.hospital import Hospital
    with app.app_context():
        hospitals = Hospital.query.all()
        hospitals_list = [hospital.to_dict() for hospital in hospitals]
        return jsonify(hospitals_list)

# get all doctors based on hospital using data get from react frontend
@app.route('/api/get_doctors', methods=['POST'])
def get_doctors():
    from db_model.doctor import Doctor
    with app.app_context():
        data = request.json
        hospital_id = data.get("hospital_id")
        doctors = Doctor.query.filter_by(hospital_id=hospital_id).all()
        doctors_list = [doctor.to_dict() for doctor in doctors]
        return jsonify(doctors_list)

# get all bedding based on hospital using data get from react frontend

@app.route('/api/get_bedding', methods=['POST'])
def get_bedding():
    from db_model.hospital import Hospital
    with app.app_context():
        data = request.json
        hospital_id = data.get("hospital_id")
        hospital = Hospital.query.filter_by(id=hospital_id).first()
        if hospital:
            bedding_info = {
                'has_emergency': hospital.has_emergency,
                'has_pediatrics': hospital.has_pediatrics,
                'has_cardiology': hospital.has_cardiology,
                'has_oncology': hospital.has_oncology,
                'has_neurology': hospital.has_neurology,
                'has_orthopedics': hospital.has_orthopedics,
                'has_radiology': hospital.has_radiology,
                'has_maternity': hospital.has_maternity,
            }
            return jsonify(bedding_info)
        else:
            return jsonify({"error": "Hospital not found"}), 404
    
# get all events
@app.route('/api/get_events', methods=['POST'])
def get_events():
    from db_model.event import Event
    with app.app_context():
        events = Event.query.all()
        events_list = [event.to_dict() for event in events]
        return jsonify(events_list)



# Example route
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from Flask backend!"})

# Example POST route
@app.route('/api/data', methods=['POST'])
def get_data():
    data = request.json
    return jsonify({"received": data})



@app.route('/')
def index():
    # test_db()
    patient = Patient.query.filter_by(email='john.doe@example.com').first()
    print("🔍 Patient as dict:", patient.to_dict())
    return "Database initialized and app running!"

if __name__ == '__main__':
    app.run(debug=True)



