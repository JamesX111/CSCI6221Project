from db_model import db, BedRecord

class BedRecordService:

    # CREATE
    @staticmethod
    def create_bed_record(data):
        """Create a new bed record. Allow manual admission_Id with collision safety."""
        try:
            custom_id = data.get("admission_Id")

            # Safety check for manual admission ID
            if custom_id is not None:
                existing = BedRecord.query.get(custom_id)
                if existing:
                    raise ValueError(f"Admission ID {custom_id} already exists.")

            new_record = BedRecord(
                admission_Id=custom_id,
                bed_No=data.get("bed_No"),
                patient_Id=data.get("patient_Id"),
                nurse_Id=data.get("nurse_Id"),
                helper_Id=data.get("helper_Id"),
                admission_Date=data.get("admission_Date"),
                discharge_Date=data.get("discharge_Date"),
                amount=data.get("amount"),
                mode_of_payment=data.get("mode_of_payment"),
            )

            db.session.add(new_record)
            db.session.commit()
            return new_record.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # UPDATE
    @staticmethod
    def update_bed_record(admission_id, data):
        """Update an existing bed record."""
        record = BedRecord.query.get(admission_id)
        if not record:
            return None

        try:
            for key, value in data.items():
                if key != "admission_Id" and hasattr(record, key):
                    setattr(record, key, value)

            db.session.commit()
            return record.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # DELETE
    @staticmethod
    def delete_bed_record(admission_id):
        """Delete a bed record."""
        record = BedRecord.query.get(admission_id)
        if not record:
            return False

        try:
            db.session.delete(record)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise e

    # GET BY BED
    @staticmethod
    def get_records_by_bed(bed_no):
        records = BedRecord.query.filter_by(bed_No=bed_no).all()
        return [r.to_dict() for r in records]

    # GET BY PATIENT
    @staticmethod
    def get_records_by_patient(patient_id):
        records = BedRecord.query.filter_by(patient_Id=patient_id).all()
        return [r.to_dict() for r in records]

    # GET BY NURSE
    @staticmethod
    def get_records_by_nurse(nurse_id):
        records = BedRecord.query.filter_by(nurse_Id=nurse_id).all()
        return [r.to_dict() for r in records]

    # GET BY HELPER
    @staticmethod
    def get_records_by_helper(helper_id):
        records = BedRecord.query.filter_by(helper_Id=helper_id).all()
        return [r.to_dict() for r in records]

    # GET ALL RECORDS
    @staticmethod
    def get_all_bed_records():
        records = BedRecord.query.all()
        return [r.to_dict() for r in records]