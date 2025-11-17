from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from db_model import db, init_db,  insert_mock_data, preinsert_departments
from flask_cors import CORS
from routes import register_routes
import pandas as pd
import json
from sqlalchemy import inspect   # <-- This is SQLAlchemy's inspector, works with Flask-SQLAlchemy

def print_db_schema(app):
    with app.app_context():
        inspector = inspect(db.engine)

        tables = inspector.get_table_names()

        print("\n=== DATABASE TABLES ===")
        for table in tables:
            print(f"\n🟦 Table: {table}")
            columns = inspector.get_columns(table)
            for col in columns:
                print(f"   - {col['name']} ({col['type']})")


app = Flask(__name__)



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



global_app = app
global_db = db
configure_app_routes()

def reset_db(app):
    """Completely reset the database (drop all tables, then recreate)."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("✅ Database has been reset!")


    



# Routes

@app.route('/api/reset_db', methods=['POST'])
def reset_database_route():
    reset_db(app)
    return jsonify({"message": "Database has been reset!"})





@ app.route('/api/insert_mock', methods=['POST'])
def insert_mock_data_route():
    # Implement the logic to insert mock data here
    insert_mock_data()
    from interfaces import StaffShiftService
    patients = StaffShiftService.get_all_shifts()
    print(f"Number of patients after mock data insertion: {len(patients)}")
    return jsonify({"message": "Mock data inserted!"})

@app.route('/')
def index():
    return "Database initialized and app running!"

if __name__ == '__main__':
    print_db_schema(app)
    with app.app_context():
        preinsert_departments()
    app.run(debug=True)



