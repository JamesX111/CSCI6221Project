from db_model import db, Ward  # Adjust import according to your project structure

class WardService:

    # CREATE
    @staticmethod
    def create_ward(data):
        try:
            custom_id = data.get("ward_No")

            # Safety check: ensure ID does not exist
            if custom_id is not None:
                existing = Ward.query.get(custom_id)
                if existing:
                    raise ValueError(f"Ward ID {custom_id} already exists.")

            ward = Ward(
                ward_No=custom_id,
                ward_Name=data["ward_Name"],
                dept_Id=data["dept_Id"]
            )

            db.session.add(ward)
            db.session.commit()
            return ward.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # UPDATE
    @staticmethod
    def update_ward(ward_no, data):
        ward = Ward.query.get(ward_no)
        if not ward:
            return None

        try:
            for key, value in data.items():
                if key != "ward_No" and hasattr(ward, key):
                    setattr(ward, key, value)

            db.session.commit()
            return ward.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # DELETE
    @staticmethod
    def delete_ward(ward_no):
        ward = Ward.query.get(ward_no)
        if not ward:
            return False

        try:
            db.session.delete(ward)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    # GET BY ID
    @staticmethod
    def get_by_id(ward_no):
        ward = Ward.query.get(ward_no)
        return ward.to_dict() if ward else None

    # GET BY DEPARTMENT
    @staticmethod
    def get_by_department(dept_id):
        wards = Ward.query.filter_by(dept_Id=dept_id).order_by(Ward.ward_Name.asc()).all()
        return [w.to_dict() for w in wards]

    # GET ALL (sorted by ward_Name)
    @staticmethod
    def get_all():
        wards = Ward.query.order_by(Ward.ward_Name.asc()).all()
        return [w.to_dict() for w in wards]
