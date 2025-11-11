from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from db_model import db, init_db
from flask_cors import CORS
from routes import register_routes
import json
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

def configure_app_routes():
    try:
        register_routes(app)
        return True
    except Exception as e:
        print(f"register fail: {str(e)}")
        return False

app = create_app()
CORS(app,
     resources={"/*": {
         "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "allow_headers": "*",
         "expose_headers": "*"
     }})


with app.app_context():
    db.create_all()

global_app = app
global_db = db
configure_app_routes()

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



# get all hospitals
@app.route('/api/get_hospitals', methods=['POST'])
def get_hospitals():
    from db_model.hospital import Hospital
    with app.app_context():
        hospitals = Hospital.query.all()
        hospitals_list = [hospital.to_dict() for hospital in hospitals]
        return jsonify(hospitals_list)




    





@app.route('/')
def index():
    
    return "Database initialized and app running!"

if __name__ == '__main__':
    app.run(debug=True)



