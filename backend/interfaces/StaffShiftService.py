from db_model import db, StaffShift

class StaffShiftService:

    # CREATE
    @staticmethod
    def create_shift(data):
        """Create a new staff shift (manual shift_Id allowed)."""
        try:
            custom_id = data.get("shift_Id")

            # Safety check for duplicate ID
            if custom_id is not None:
                existing = StaffShift.query.get(custom_id)
                if existing:
                    raise ValueError(f"Shift ID {custom_id} already exists.")

            shift = StaffShift(
                shift_Id=custom_id,
                doct_Id=data.get("doct_Id"),
                nurse_Id=data.get("nurse_Id"),
                helper_Id=data.get("helper_Id"),
                shift_Date=data["shift_Date"],
                shift_Start=data["shift_Start"],
                shift_End=data["shift_End"]
            )

            db.session.add(shift)
            db.session.commit()
            return shift.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # UPDATE
    @staticmethod
    def update_shift(shift_id, data):
        shift = StaffShift.query.get(shift_id)
        if not shift:
            return None

        try:
            for key, value in data.items():
                if key != "shift_Id" and hasattr(shift, key):
                    setattr(shift, key, value)

            db.session.commit()
            return shift.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # DELETE
    @staticmethod
    def delete_shift(shift_id):
        shift = StaffShift.query.get(shift_id)
        if not shift:
            return False

        try:
            db.session.delete(shift)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise e

    # GET ALL (sorted by shift_Date then shift_Start)
    @staticmethod
    def get_all_shifts():
        shifts = StaffShift.query.order_by(StaffShift.shift_Date.asc(), StaffShift.shift_Start.asc()).all()
        return [s.to_dict() for s in shifts]

    # GET BY DOCTOR
    @staticmethod
    def get_by_doctor(doct_id):
        shifts = (
            StaffShift.query
            .filter_by(doct_Id=doct_id)
            .order_by(StaffShift.shift_Date.asc(), StaffShift.shift_Start.asc())
            .all()
        )
        return [s.to_dict() for s in shifts]

    # GET BY NURSE
    @staticmethod
    def get_by_nurse(nurse_id):
        shifts = (
            StaffShift.query
            .filter_by(nurse_Id=nurse_id)
            .order_by(StaffShift.shift_Date.asc(), StaffShift.shift_Start.asc())
            .all()
        )
        return [s.to_dict() for s in shifts]

    # GET BY HELPER
    @staticmethod
    def get_by_helper(helper_id):
        shifts = (
            StaffShift.query
            .filter_by(helper_Id=helper_id)
            .order_by(StaffShift.shift_Date.asc(), StaffShift.shift_Start.asc())
            .all()
        )
        return [s.to_dict() for s in shifts]
    # GET BY ID
    @staticmethod
    def get_shift_by_id(shift_id):
        """Retrieve staff shift by primary key."""
        shift = StaffShift.query.get(shift_id)
        return shift.to_dict() if shift else None