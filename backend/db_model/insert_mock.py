from .  import db
import pandas as pd
from datetime import datetime, date



def insert_mock_data(file_path='Data/Hospital_Management_System.xlsx', num_rows=20):
    """Insert mock data from an Excel file into the database safely and avoid duplicates."""
    xls = pd.ExcelFile(file_path)

    # ----------- Patient data -----------
    df_patient = pd.read_excel(xls, 'Patients').head(num_rows)
    from .Patient import Patient

    for _, row in df_patient.iterrows():
        if pd.isnull(row.get('patient_Id')):
            # print(f"Skipping patient row due to missing patient_Id: {row.to_dict()}")
            continue

        # Skip if patient already exists
        exists = Patient.query.filter_by(patient_Id=row['patient_Id']).first()
        if exists:
            # print(f"Skipping patient {row['patient_Id']}, already exists.")
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
            # print(f"Skipping ward row due to missing ward_No: {row.to_dict()}")
            continue

        # Skip if ward already exists
        exists = Ward.query.filter_by(ward_No=row['ward_No']).first()
        if exists:
            # print(f"Skipping ward {row['ward_No']}, already exists.")
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
            # print(f"Skipping doctor row due to missing doct_Id: {row.to_dict()}")
            continue

        # Skip if doctor already exists
        exists = Doctor.query.filter_by(doct_Id=row['doct_Id']).first()
        if exists:
            # print(f"Skipping doctor {row['doct_Id']}, already exists.")
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

    # ----------- Nurse data -----------
    df_nurse = pd.read_excel(xls, 'Nurse').head(num_rows)
    from .Nurse import Nurse

    for _, row in df_nurse.iterrows():
        if pd.isnull(row.get('nurse_Id')):
            # print(f"Skipping nurse row due to missing nurse_Id: {row.to_dict()}")
            continue

        exists = Nurse.query.filter_by(nurse_Id=row['nurse_Id']).first()
        if exists:
            # print(f"Skipping nurse {row['nurse_Id']}, already exists.")
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

    # ----------- BedRecord data -----------
    df_bed_record = pd.read_excel(xls, 'BedRecords').head(num_rows)
    from .BedRecord import BedRecord

    for _, row in df_bed_record.iterrows():
        if pd.isnull(row.get('admission_Id')):
            # print(f"Skipping bed record row due to missing admission_Id: {row.to_dict()}")
            continue

        exists = BedRecord.query.filter_by(admission_Id=row['admission_Id']).first()
        if exists:
            # print(f"Skipping bed record {row['admission_Id']}, already exists.")
            continue

        bed_record = BedRecord(
            admission_Id=row['admission_Id'],
            bed_No=row['bed_No'],
            patient_Id=row['patient_Id'],
            nurse_Id=row.get('nurse_Id'),
            helper_Id=row.get('helper_Id'),
            admission_Date=row['admission_Date'],
            discharge_Date=row.get('discharge_Date'),
            amount=row.get('amount'),
            mode_of_payment=row.get('mode_of_payment')
        )
        db.session.add(bed_record)

    db.session.commit()

    # ----------- RoomRecord data -----------
    df_room_record = pd.read_excel(xls, 'RoomRecords').head(num_rows)
    from .RoomRecord import RoomRecord

    for _, row in df_room_record.iterrows():
        if pd.isnull(row.get('admission_ID')):
            # print(f"Skipping room record row due to missing admission_ID: {row.to_dict()}")
            continue

        exists = RoomRecord.query.filter_by(admission_ID=row['admission_ID']).first()
        if exists:
            # print(f"Skipping room record {row['admission_ID']}, already exists.")
            continue

        room_record = RoomRecord(
            admission_ID=row['admission_ID'],
            room_no=row['room_no'],
            patient_Id=row['patient_Id'],
            nurse_Id=row.get('nurse_Id'),
            helper_Id=row.get('helper_Id'),
            admission_Date=row['admission_Date'],
            discharge_Date=row.get('discharge_Date'),
            amount=row.get('amount'),
            mode_of_payment=row.get('mode_of_payment')
        )
        db.session.add(room_record)

    db.session.commit()

    # ----------- SurgeryRecord data -----------
    df_surgery_record = pd.read_excel(xls, 'SurgeryRecord').head(num_rows)
    from .SurgeryRecord import SurgeryRecord

    for _, row in df_surgery_record.iterrows():
        if pd.isnull(row.get('surgery_Id')):
            print(f"Skipping surgery record row due to missing surgery_Id: {row.to_dict()}")
            continue

        exists = SurgeryRecord.query.filter_by(surgery_Id=row['surgery_Id']).first()
        if exists:
            # print(f"Skipping surgery record {row['surgery_Id']}, already exists.")
            continue

        # Convert surgery_Date to date
        surgery_date = row['surgery_Date']
        if pd.notnull(surgery_date):
            if isinstance(surgery_date, pd.Timestamp):
                surgery_date = surgery_date.date()
            elif isinstance(surgery_date, str):
                try:
                    surgery_date = datetime.strptime(surgery_date, "%Y-%m-%d").date()
                except Exception:
                    print(f"Invalid surgery_Date for surgery {row['surgery_Id']}, skipping.")
                    continue
        else:
            print(f"Missing surgery_Date for surgery {row['surgery_Id']}, skipping.")
            continue

        # Convert start_Time and end_Time to time
        def to_time(val, field_name):
            if pd.isnull(val):
                return None
            if isinstance(val, pd.Timestamp):
                return val.time()
            if isinstance(val, str):
                try:
                    return datetime.strptime(val, "%H:%M:%S").time()
                except Exception:
                    print(f"Invalid {field_name} for surgery {row['surgery_Id']}, skipping.")
                    return None
            if isinstance(val, datetime):
                return val.time()
            return val  # assume it's already a time object

        start_time = to_time(row['start_Time'], 'start_Time')
        end_time = to_time(row['end_Time'], 'end_Time')
        if start_time is None or end_time is None:
            continue

        surgery_record = SurgeryRecord(
            surgery_Id=row['surgery_Id'],
            patient_Id=row['patient_Id'],
            surgeon_Id=row['surgeon_Id'],
            surgery_Type=row['surgery_Type'],
            surgery_Date=surgery_date,
            start_Time=start_time,
            end_Time=end_time,
            room_no=row.get('room_no'),
            notes=row.get('notes'),
            nurse_Id=row.get('nurse_Id'),
            helper_Id=row.get('helper_Id')
        )
        db.session.add(surgery_record)

    db.session.commit()

    # ----------- StaffShift data -----------
    df_staff_shift = pd.read_excel(xls, 'StaffShift').head(num_rows)
    from .StaffShift import StaffShift

    for _, row in df_staff_shift.iterrows():
        if pd.isnull(row.get('shift_Id')):
            print(f"Skipping staff shift row due to missing shift_Id: {row.to_dict()}")
            continue

        exists = StaffShift.query.filter_by(shift_Id=row['shift_Id']).first()
        if exists:
            # print(f"Skipping staff shift {row['shift_Id']}, already exists.")
            continue

        # Convert shift_Date to date
        shift_date = row['shift_Date']
        if pd.notnull(shift_date):
            if isinstance(shift_date, pd.Timestamp):
                shift_date = shift_date.date()
            elif isinstance(shift_date, str):
                try:
                    shift_date = datetime.strptime(shift_date, "%Y-%m-%d").date()
                except Exception:
                    print(f"Invalid shift_Date for shift {row['shift_Id']}, skipping.")
                    continue
        else:
            print(f"Missing shift_Date for shift {row['shift_Id']}, skipping.")
            continue

        # Convert shift_Start and shift_End to time
        def to_time(val, field_name):
            if pd.isnull(val):
                return None
            if isinstance(val, pd.Timestamp):
                return val.time()
            if isinstance(val, str):
                try:
                    return datetime.strptime(val, "%H:%M:%S").time()
                except Exception:
                    print(f"Invalid {field_name} for shift {row['shift_Id']}, skipping.")
                    return None
            if isinstance(val, datetime):
                return val.time()
            return val  # assume it's already a time object

        shift_start = to_time(row['shift_Start'], 'shift_Start')
        shift_end = to_time(row['shift_End'], 'shift_End')
        if shift_start is None or shift_end is None:
            continue

        staff_shift = StaffShift(
            shift_Id=row['shift_Id'],
            doct_Id=row.get('doct_Id'),
            nurse_Id=row.get('nurse_Id'),
            helper_Id=row.get('helper_Id'),
            shift_Date=shift_date,
            shift_Start=shift_start,
            shift_End=shift_end
        )
        db.session.add(staff_shift)

    db.session.commit()

    # ----------- MedicalRecord data -----------
    df_medical_record = pd.read_excel(xls, 'MedicalRecord').head(num_rows)
    from .MedicalRecord import MedicalRecord

    for _, row in df_medical_record.iterrows():

        if pd.isnull(row.get('record_Id')):
            print(f"Skipping medical record row due to missing record_Id: {row.to_dict()}")
            continue

        # Skip if record already exists
        exists = MedicalRecord.query.filter_by(record_Id=row['record_Id']).first()
        if exists:
            # print(f"Skipping medical record {row['record_Id']}, already exists.")
            continue

        # --- Convert visit_Date ---
        visit_date = row.get('visit_Date')
        if pd.notnull(visit_date):
            if isinstance(visit_date, pd.Timestamp):
                visit_date = visit_date.to_pydatetime()
            elif isinstance(visit_date, str):
                try:
                    visit_date = datetime.strptime(visit_date, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    try:
                        visit_date = datetime.strptime(visit_date, "%Y-%m-%d")
                    except Exception:
                        print(f"Invalid visit_Date for record {row['record_Id']}, skipping.")
                        continue
        else:
            print(f"Missing visit_Date for record {row['record_Id']}, skipping.")
            continue

        # --- Convert next_Visit ---
        next_visit = row.get('next_Visit')
        if pd.notnull(next_visit):
            if isinstance(next_visit, pd.Timestamp):
                next_visit = next_visit.to_pydatetime()
            elif isinstance(next_visit, str):
                try:
                    next_visit = datetime.strptime(next_visit, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    try:
                        next_visit = datetime.strptime(next_visit, "%Y-%m-%d")
                    except Exception:
                        print(f"Invalid next_Visit for record {row['record_Id']}, setting to None.")
                        next_visit = None
        else:
            next_visit = None

        medical_record = MedicalRecord(
            record_Id=row['record_Id'],
            doct_Id=row['doct_Id'],
            patient_Id=row['patient_Id'],
            visit_Date=visit_date,
            curr_Weight=row.get('curr_Weight'),
            curr_height=row.get('curr_height'),
            curr_Blood_Pressure=row.get('curr_Blood_Pressure'),
            curr_Temp_F=row.get('curr_Temp_F'),
            diagnosis=row.get('diagnosis'),
            treatment=row.get('treatment'),
            next_Visit=next_visit
        )

        db.session.add(medical_record)

    db.session.commit()

    
    # ----------- Bed data -----------
    df_bed = pd.read_excel(xls, 'Bed').head(num_rows)
    from .Bed import Bed

    for _, row in df_bed.iterrows():
        if pd.isnull(row.get('bed_No')):
            print(f"Skipping bed row due to missing bed_No: {row.to_dict()}")
            continue

        # Skip if bed already exists
        exists = Bed.query.filter_by(bed_No=row['bed_No']).first()
        if exists:
            print(f"Skipping bed {row['bed_No']}, already exists.")
            continue

        bed = Bed(
            bed_No=int(row['bed_No']),
            ward_No=int(row['ward_No']),
            available=row.get('available', "Available")  # defaults to "Available"
        )

        db.session.add(bed)

    db.session.commit()



    print("✅ Mock data inserted successfully, duplicates skipped.")
