from db_model import db, RoomRecord

class RoomRecordService:

    # CREATE
    @staticmethod
    def create_record(data):
        """Create a new room record (manual admission_ID allowed)."""
        try:
            custom_id = data.get("admission_ID")

            # Collision check
            if custom_id is not None:
                existing = RoomRecord.query.get(custom_id)
                if existing:
                    raise ValueError(f"Admission ID {custom_id} already exists.")

            record = RoomRecord(
                admission_ID=custom_id,
                room_no=data["room_no"],
                patient_Id=data["patient_Id"],
                nurse_Id=data.get("nurse_Id"),
                helper_Id=data.get("helper_Id"),
                admission_Date=data.get("admission_Date"),
                discharge_Date=data.get("discharge_Date"),
                amount=data.get("amount"),
                mode_of_payment=data.get("mode_of_payment")
            )

            db.session.add(record)
            db.session.commit()
            return record.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # UPDATE
    @staticmethod
    def update_record(admission_id, data):
        record = RoomRecord.query.get(admission_id)
        if not record:
            return None

        try:
            for key, value in data.items():
                if key != "admission_ID" and hasattr(record, key):
                    setattr(record, key, value)

            db.session.commit()
            return record.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # DELETE
    @staticmethod
    def delete_record(admission_id):
        record = RoomRecord.query.get(admission_id)
        if not record:
            return False

        try:
            db.session.delete(record)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise e

    # GET ALL (sorted by admission_ID)
    @staticmethod
    def get_all_records():
        records = RoomRecord.query.order_by(RoomRecord.admission_ID.asc()).all()
        return [r.to_dict() for r in records]

    # GET BY ADMISSION ID
    @staticmethod
    def get_by_admission_id(admission_id):
        record = RoomRecord.query.get(admission_id)
        return record.to_dict() if record else None

    # GET BY PATIENT
    @staticmethod
    def get_by_patient(patient_id):
        records = (
            RoomRecord.query
            .filter_by(patient_Id=patient_id)
            .order_by(RoomRecord.admission_ID.asc())
            .all()
        )
        return [r.to_dict() for r in records]

    # GET BY NURSE
    @staticmethod
    def get_by_nurse(nurse_id):
        records = (
            RoomRecord.query
            .filter_by(nurse_Id=nurse_id)
            .order_by(RoomRecord.admission_ID.asc())
            .all()
        )
        return [r.to_dict() for r in records]

    # GET BY HELPER
    @staticmethod
    def get_by_helper(helper_id):
        records = (
            RoomRecord.query
            .filter_by(helper_Id=helper_id)
            .order_by(RoomRecord.admission_ID.asc())
            .all()
        )
        return [r.to_dict() for r in records]
    
    # GET BY ROOM NO
    @staticmethod
    def get_by_room_no(room_no):
        records = (
            RoomRecord.query
            .filter_by(room_no=room_no)
            .order_by(RoomRecord.admission_ID.asc())
            .all()
        )
        return [r.to_dict() for r in records]