from db_model import db, Helper

class HelperService:

    # CREATE
    @staticmethod
    def create_helper(data):
        """Create a new helper (manual helper_Id allowed with safety check)."""
        try:
            custom_id = data.get("helper_Id")

            # Safety check: prevent duplicate primary key
            if custom_id is not None:
                existing = Helper.query.get(custom_id)
                if existing:
                    raise ValueError(f"Helper ID {custom_id} already exists.")

            new_helper = Helper(
                helper_Id=custom_id,
                dept_Id=data.get("dept_Id"),
                FName=data.get("FName"),
                LName=data.get("LName"),
                Gender=data.get("Gender"),
                contact_No=data.get("contact_No"),
            )

            db.session.add(new_helper)
            db.session.commit()
            return new_helper.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # UPDATE
    @staticmethod
    def update_helper(helper_id, data):
        helper = Helper.query.get(helper_id)
        if not helper:
            return None

        try:
            for key, value in data.items():
                if key != "helper_Id" and hasattr(helper, key):
                    setattr(helper, key, value)

            db.session.commit()
            return helper.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # DELETE
    @staticmethod
    def delete_helper(helper_id):
        helper = Helper.query.get(helper_id)
        if not helper:
            return False

        try:
            db.session.delete(helper)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise e

    # GET BY ID
    @staticmethod
    def get_helper_by_id(helper_id):
        helper = Helper.query.get(helper_id)
        return helper.to_dict() if helper else None

    # GET BY GENDER (sorted alphabetically)
    @staticmethod
    def get_helpers_by_gender(gender):
        helpers = (
            Helper.query
            .filter_by(Gender=gender)
            .order_by(Helper.LName.asc())
            .all()
        )
        return [h.to_dict() for h in helpers]

    # GET BY DEPARTMENT (sorted alphabetically)
    @staticmethod
    def get_helpers_by_department(dept_id):
        helpers = (
            Helper.query
            .filter_by(dept_Id=dept_id)
            .order_by(Helper.LName.asc())
            .all()
        )
        return [h.to_dict() for h in helpers]




    @staticmethod
    def get_all_helpers():
        helpers = Helper.query.order_by(Helper.LName.asc()).all()
        return [h.to_dict() for h in helpers]
