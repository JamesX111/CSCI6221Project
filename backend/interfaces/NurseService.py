from db_model import db, Nurse

class NurseService:

    # CREATE
    @staticmethod
    def create_nurse(data):
        """Create a new nurse (manual nurse_Id allowed with safety check)."""
        try:
            custom_id = data.get("nurse_Id")

            # Prevent duplicate ID
            if custom_id is not None:
                existing = Nurse.query.get(custom_id)
                if existing:
                    raise ValueError(f"Nurse ID {custom_id} already exists.")

            new_nurse = Nurse(
                nurse_Id=custom_id,
                dept_Id=data.get("dept_Id"),
                FName=data.get("FName"),
                LName=data.get("LName"),
                Gender=data.get("Gender"),
                conatct_No=data.get("conatct_No"),  # Must match model typo
            )

            db.session.add(new_nurse)
            db.session.commit()
            return new_nurse.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # UPDATE
    @staticmethod
    def update_nurse(nurse_id, data):
        nurse = Nurse.query.get(nurse_id)
        if not nurse:
            return None

        try:
            for key, value in data.items():
                if key != "nurse_Id" and hasattr(nurse, key):
                    setattr(nurse, key, value)

            db.session.commit()
            return nurse.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # DELETE
    @staticmethod
    def delete_nurse(nurse_id):
        nurse = Nurse.query.get(nurse_id)
        if not nurse:
            return False

        try:
            db.session.delete(nurse)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise e

    # GET BY ID
    @staticmethod
    def get_nurse_by_id(nurse_id):
        nurse = Nurse.query.get(nurse_id)
        return nurse.to_dict() if nurse else None

    # GET BY GENDER (sorted alphabetically)
    @staticmethod
    def get_nurses_by_gender(gender):
        nurses = (
            Nurse.query
            .filter_by(Gender=gender)
            .order_by(Nurse.LName.asc())
            .all()
        )
        return [n.to_dict() for n in nurses]

    # GET BY DEPARTMENT (sorted alphabetically)
    @staticmethod
    def get_nurses_by_department(dept_id):
        nurses = (
            Nurse.query
            .filter_by(dept_Id=dept_id)
            .order_by(Nurse.LName.asc())
            .all()
        )
        return [n.to_dict() for n in nurses]

    # GET ALL SORTED BY LAST NAME
    @staticmethod
    def get_all_sorted_by_lastname():
        nurses = Nurse.query.order_by(Nurse.LName.asc()).all()
        return [n.to_dict() for n in nurses]

    # OPTIONAL: GET ALL
    @staticmethod
    def get_all_nurses():
        nurses = Nurse.query.order_by(Nurse.LName.asc()).all()
        return [n.to_dict() for n in nurses]
