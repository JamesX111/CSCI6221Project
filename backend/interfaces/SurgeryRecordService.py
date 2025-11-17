from db_model import db
from db_model import SurgeryRecord  # Adjust import according to your project structure

class SurgeryRecordService:

    # CREATE
    @staticmethod
    def create_surgery(data):
        """Create a new surgery record."""
        try:
            custom_id = data.get("surgery_Id")

            # Safety check: ensure ID does not exist
            if custom_id is not None:
                existing = SurgeryRecord.query.get(custom_id)
                if existing:
                    raise ValueError(f"Surgery ID {custom_id} already exists.")

            surgery = SurgeryRecord(
                surgery_Id=custom_id,
                patient_Id=data["patient_Id"],
                surgeon_Id=data["surgeon_Id"],
                surgery_Type=data["surgery_Type"],
                surgery_Date=data["surgery_Date"],
                start_Time=data["start_Time"],
                end_Time=data["end_Time"],
                room_no=data.get("room_no"),
                notes=data.get("notes"),
                nurse_Id=data.get("nurse_Id"),
                helper_Id=data.get("helper_Id")
            )

            db.session.add(surgery)
            db.session.commit()
            return surgery.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # UPDATE
    @staticmethod
    def update_surgery(surgery_id, data):
        surgery = SurgeryRecord.query.get(surgery_id)
        if not surgery:
            return None

        try:
            for key, value in data.items():
                if key != "surgery_Id" and hasattr(surgery, key):
                    setattr(surgery, key, value)

            db.session.commit()
            return surgery.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # DELETE
    @staticmethod
    def delete_surgery(surgery_id):
        surgery = SurgeryRecord.query.get(surgery_id)
        if not surgery:
            return False

        try:
            db.session.delete(surgery)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    # GET BY ID
    @staticmethod
    def get_by_id(surgery_id):
        surgery = SurgeryRecord.query.get(surgery_id)
        return surgery.to_dict() if surgery else None

    # GET ALL (sorted by surgery_Date then start_Time)
    @staticmethod
    def get_all():
        surgeries = SurgeryRecord.query.order_by(
            SurgeryRecord.surgery_Date.asc(),
            SurgeryRecord.start_Time.asc()
        ).all()
        return [s.to_dict() for s in surgeries]

    # GET BY PATIENT
    @staticmethod
    def get_by_patient(patient_id):
        surgeries = SurgeryRecord.query.filter_by(patient_Id=patient_id).order_by(
            SurgeryRecord.surgery_Date.asc(),
            SurgeryRecord.start_Time.asc()
        ).all()
        return [s.to_dict() for s in surgeries]

    # GET BY DOCTOR / SURGEON
    @staticmethod
    def get_by_doctor(doctor_id):
        surgeries = SurgeryRecord.query.filter_by(surgeon_Id=doctor_id).order_by(
            SurgeryRecord.surgery_Date.asc(),
            SurgeryRecord.start_Time.asc()
        ).all()
        return [s.to_dict() for s in surgeries]

    # GET BY NURSE
    @staticmethod
    def get_by_nurse(nurse_id):
        surgeries = SurgeryRecord.query.filter_by(nurse_Id=nurse_id).order_by(
            SurgeryRecord.surgery_Date.asc(),
            SurgeryRecord.start_Time.asc()
        ).all()
        return [s.to_dict() for s in surgeries]

    # GET BY HELPER
    @staticmethod
    def get_by_helper(helper_id):
        surgeries = SurgeryRecord.query.filter_by(helper_Id=helper_id).order_by(
            SurgeryRecord.surgery_Date.asc(),
            SurgeryRecord.start_Time.asc()
        ).all()
        return [s.to_dict() for s in surgeries]
    
    # GET BY SURGERY TYPE
    @staticmethod
    def get_by_surgery_type(surgery_type):
        surgeries = SurgeryRecord.query.filter_by(surgery_Type=surgery_type).order_by(
            SurgeryRecord.surgery_Date.asc(),
            SurgeryRecord.start_Time.asc()
        ).all()
        return [s.to_dict() for s in surgeries]