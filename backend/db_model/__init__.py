import os
import pandas as pd
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def insert_mock_data(file_path='Data/Hospital_Management_System.xlsx', num_rows=20):
    """Insert mock data from an Excel file into the database safely and avoid duplicates."""
    xls = pd.ExcelFile(file_path)

    # ----------- Patient data -----------
    df_patient = pd.read_excel(xls, 'Patients').head(num_rows)
    from .Patient import Patient

    for _, row in df_patient.iterrows():
        if pd.isnull(row.get('patient_Id')):
            print(f"Skipping patient row due to missing patient_Id: {row.to_dict()}")
            continue

        # Skip if patient already exists
        exists = Patient.query.filter_by(patient_Id=row['patient_Id']).first()
        if exists:
            print(f"Skipping patient {row['patient_Id']}, already exists.")
            continue

        # Safely handle Date_Of_Birth
        dob = row['Date_Of_Birth']
        if pd.notnull(dob):
            if isinstance(dob, pd.Timestamp):
                dob = dob.date()
            elif isinstance(dob, str):
                try:
                    dob = datetime.strptime(dob, '%Y-%m-%d').date()
                except Exception:
                    print(f"Invalid date format for patient {row['patient_Id']}, skipping.")
                    continue
        else:
            print(f"Missing Date_Of_Birth for patient {row['patient_Id']}, skipping.")
            continue

        patient = Patient(
            patient_Id=row['patient_Id'],
            FName=row['FName'],
            LName=row['LName'],
            Date_Of_Birth=dob,
            Gender=row['Gender'],
            contact_No=row['contact_No'],
            pt_Address=row['pt_Address']
        )
        db.session.add(patient)

    db.session.commit()

    # ----------- Ward data -----------
    df_ward = pd.read_excel(xls, 'Ward').head(num_rows)
    from .Ward import Ward

    for _, row in df_ward.iterrows():
        if pd.isnull(row.get('ward_No')):
            print(f"Skipping ward row due to missing ward_No: {row.to_dict()}")
            continue

        # Skip if ward already exists
        exists = Ward.query.filter_by(ward_No=row['ward_No']).first()
        if exists:
            print(f"Skipping ward {row['ward_No']}, already exists.")
            continue

        ward = Ward(
            ward_No=row['ward_No'],
            ward_Name=row['ward_Name'],
            dept_Id=row['dept_Id']
        )
        db.session.add(ward)

    db.session.commit()

    # ----------- Doctor data -----------
    df_doctor = pd.read_excel(xls, 'Doctor').head(num_rows)
    from .Doctor import Doctor

    for _, row in df_doctor.iterrows():
        if pd.isnull(row.get('doct_Id')):
            print(f"Skipping doctor row due to missing doct_Id: {row.to_dict()}")
            continue

        # Skip if doctor already exists
        exists = Doctor.query.filter_by(doct_Id=row['doct_Id']).first()
        if exists:
            print(f"Skipping doctor {row['doct_Id']}, already exists.")
            continue

        doctor = Doctor(
            doct_Id=row['doct_Id'],
            dept_Id=row['dept_Id'],
            FName=row['FName'],
            LName=row['LName'],
            Gender=row['Gender'],
            contact_No=row['contact_No'],
            surgeon_Type=row.get('surgeon_Type'),  # optional
            office_No=row.get('office_No')         # optional
        )
        db.session.add(doctor)

    db.session.commit()

    # ---- -------- Helper data -----------
    df_helper = pd.read_excel(xls, 'Helpers').head(num_rows)
    from .Helper import Helper
    for _, row in df_helper.iterrows():
        if pd.isnull(row.get('helper_Id')):
            print(f"Skipping helper row due to missing helper_Id: {row.to_dict()}")
            continue

        # Skip if helper already exists
        exists = Helper.query.filter_by(helper_Id=row['helper_Id']).first()
        if exists:
            print(f"Skipping helper {row['helper_Id']}, already exists.")
            continue

        helper = Helper(
            helper_Id=row['helper_Id'],
            dept_Id=row['dept_Id'],
            FName=row['FName'],
            LName=row['LName'],
            Gender=row['Gender'],
            contact_No=row['contact_No']
        )
        db.session.add(helper)
    db.session.commit()



    # ----------- Nurse data -----------
    df_nurse = pd.read_excel(xls, 'Nurse').head(num_rows)
    from .Nurse import Nurse

    for _, row in df_nurse.iterrows():
        if pd.isnull(row.get('nurse_Id')):
            print(f"Skipping nurse row due to missing nurse_Id: {row.to_dict()}")
            continue

        exists = Nurse.query.filter_by(nurse_Id=row['nurse_Id']).first()
        if exists:
            print(f"Skipping nurse {row['nurse_Id']}, already exists.")
            continue

        nurse = Nurse(
            nurse_Id=row['nurse_Id'],
            dept_Id=row['dept_Id'],
            FName=row['FName'],
            LName=row['LName'],
            Gender=row['Gender'],
            conatct_No=row.get('conatct_No')  # optional
        )
        db.session.add(nurse)

    db.session.commit()


    print("✅ Mock data inserted successfully, duplicates skipped.")



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


