from db_model import db, MedicalRecord

class MedicalRecordService:

    # CREATE
    @staticmethod
    def create_medical_record(data):
        """Create a new medical record (manual record_Id allowed with safety check)."""
        try:
            custom_id = data.get("record_Id")

            # Collision check
            if custom_id is not None:
                existing = MedicalRecord.query.get(custom_id)
                if existing:
                    raise ValueError(f"MedicalRecord ID {custom_id} already exists.")

            new_record = MedicalRecord(
                record_Id=custom_id,
                doct_Id=data.get("doct_Id"),
                patient_Id=data.get("patient_Id"),
                visit_Date=data.get("visit_Date"),
                curr_Weight=data.get("curr_Weight"),
                curr_height=data.get("curr_height"),
                curr_Blood_Pressure=data.get("curr_Blood_Pressure"),
                curr_Temp_F=data.get("curr_Temp_F"),
                diagnosis=data.get("diagnosis"),
                treatment=data.get("treatment"),
                next_Visit=data.get("next_Visit")
            )

            db.session.add(new_record)
            db.session.commit()
            return new_record.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # UPDATE
    @staticmethod
    def update_medical_record(record_id, data):
        record = MedicalRecord.query.get(record_id)
        if not record:
            return None

        try:
            for key, value in data.items():
                if key != "record_Id" and hasattr(record, key):
                    setattr(record, key, value)

            db.session.commit()
            return record.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # DELETE
    @staticmethod
    def delete_medical_record(record_id):
        record = MedicalRecord.query.get(record_id)
        if not record:
            return False

        try:
            db.session.delete(record)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise e

    # GET BY ID
    @staticmethod
    def get_medical_record_by_id(record_id):
        record = MedicalRecord.query.get(record_id)
        return record.to_dict() if record else None

    # GET BY DOCTOR (sorted by visit_Date descending)
    @staticmethod
    def get_medical_records_by_doctor(doct_id):
        records = (
            MedicalRecord.query
            .filter_by(doct_Id=doct_id)
            .order_by(MedicalRecord.visit_Date.desc())
            .all()
        )
        return [r.to_dict() for r in records]

    # GET BY PATIENT (sorted by visit_Date descending)
    @staticmethod
    def get_medical_records_by_patient(patient_id):
        records = (
            MedicalRecord.query
            .filter_by(patient_Id=patient_id)
            .order_by(MedicalRecord.visit_Date.desc())
            .all()
        )
        return [r.to_dict() for r in records]

    # GET ALL RECORDS (sorted by visit_Date descending)
    @staticmethod
    def get_all_medical_records():
        records = MedicalRecord.query.order_by(MedicalRecord.visit_Date.desc()).all()
        return [r.to_dict() for r in records]