from db_model import db, Doctor

class DoctorService:

    # CREATE
    @staticmethod
    def create_doctor(data):
        """Create a new doctor (manual doct_Id allowed with safety check)."""
        try:
            custom_id = data.get("doct_Id")

            # Safety check to avoid duplicate primary key
            if custom_id is not None:
                existing = Doctor.query.get(custom_id)
                if existing:
                    raise ValueError(f"Doctor ID {custom_id} already exists.")

            new_doctor = Doctor(
                doct_Id=custom_id,
                dept_Id=data.get("dept_Id"),
                FName=data.get("FName"),
                LName=data.get("LName"),
                Gender=data.get("Gender"),
                contact_No=data.get("contact_No"),
                surgeon_Type=data.get("surgeon_Type"),
                office_No=data.get("office_No"),
            )

            db.session.add(new_doctor)
            db.session.commit()
            return new_doctor.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # UPDATE
    @staticmethod
    def update_doctor(doctor_id, data):
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return None

        try:
            for key, value in data.items():
                if key != "doct_Id" and hasattr(doctor, key):
                    setattr(doctor, key, value)

            db.session.commit()
            return doctor.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # DELETE
    @staticmethod
    def delete_doctor(doctor_id):
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return False

        try:
            db.session.delete(doctor)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise e

    # GET BY ID
    @staticmethod
    def get_doctor_by_id(doctor_id):
        doctor = Doctor.query.get(doctor_id)
        return doctor.to_dict() if doctor else None

    # GET BY GENDER (sorted alphabetically)
    @staticmethod
    def get_doctors_by_gender(gender):
        doctors = (
            Doctor.query
            .filter_by(Gender=gender)
            .order_by(Doctor.LName.asc())
            .all()
        )
        return [d.to_dict() for d in doctors]

    # GET BY DEPARTMENT (sorted alphabetically)
    @staticmethod
    def get_doctors_by_department(dept_id):
        doctors = (
            Doctor.query
            .filter_by(dept_Id=dept_id)
            .order_by(Doctor.LName.asc())
            .all()
        )
        return [d.to_dict() for d in doctors]


    @staticmethod
    def get_all_doctors():
        doctors = Doctor.query.order_by(Doctor.LName.asc()).all()
        return [d.to_dict() for d in doctors]
