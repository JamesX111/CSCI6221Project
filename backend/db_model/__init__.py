import os
import pandas as pd
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()






def preinsert_departments():
    
    departments = [
        (101, "Cardiology"),
        (102, "Neurology"),
        (103, "Gastroenterology"),
        (104, "Nephrology"),
        (105, "Pulmonology"),
        (106, "Endocrinology"),
        (107, "General Medicine"),
        (108, "Pediatrics"),
        (109, "Orthopedics"),
        (110, "Gynecology"),
        (111, "Dentistry"),
        (112, "Dermatology"),
        (113, "Psychiatry"),
        (114, "Psychology"),
        (115, "Urology"),
        (116, "ENT"),
        (117, "Surgery"),
        (118, "Radiology"),
        (119, "Oncology"),
        (120, "Anesthesiology"),
        (121, "Emergency Medicine"),
        (122, "Nutrition & Dietetics"),
        (123, "Rehabilitation"),
        (124, "Hematology"),
        (125, "Immunology"),
        (126, "Audiology & Speech"),
        (127, "Homeopathy"),
        (128, "Sexology"),
        (129, "Family Medicine"),
        (130, "Critical Care"),
        (131, "Geriatrics"),
    ]

    for dept_id, dept_name in departments:
        # Check if department already exists
        exists = Department.query.filter_by(dept_Id=dept_id).first()
        if not exists:
            dept = Department(dept_Id=dept_id, dept_Name=dept_name)
            db.session.add(dept)

    db.session.commit()



def init_db(app):
    db.init_app(app)

    with app.app_context():
        db.create_all() 


    print("✔ Database, routes, interfaces fully generated!")


from .insert_mock import insert_mock_data

from .Appointment import Appointment
from .Bed import Bed
from .BedRecord import BedRecord
from .Doctor import Doctor

from .Department import Department
from .Helper import Helper
from .MedicalRecord import MedicalRecord
from .Nurse import Nurse
from .Patient import Patient
from .Room import Room
from .RoomRecord import RoomRecord
from .StaffShift import StaffShift
from .SurgeryRecord import SurgeryRecord
from .Ward import Ward


