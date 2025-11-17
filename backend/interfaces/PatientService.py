from db_model import db, Patient

class PatientService:

    # CREATE
    @staticmethod
    def create_patient(data):
        """Create a new patient (manual patient_Id allowed with collision safety)."""
        try:
            custom_id = data.get("patient_Id")

            # Collision check if manual ID is provided
            if custom_id is not None:
                existing = Patient.query.get(custom_id)
                if existing:
                    raise ValueError(f"Patient ID {custom_id} already exists.")

            new_patient = Patient(
                patient_Id=custom_id,
                FName=data.get("FName"),
                LName=data.get("LName"),
                Gender=data.get("Gender"),
                Date_Of_Birth=data.get("Date_Of_Birth"),
                contact_No=data.get("contact_No"),
                pt_Address=data.get("pt_Address")
            )

            db.session.add(new_patient)
            db.session.commit()
            return new_patient.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # UPDATE
    @staticmethod
    def update_patient(patient_id, data):
        patient = Patient.query.get(patient_id)
        if not patient:
            return None

        try:
            for key, value in data.items():
                if key != "patient_Id" and hasattr(patient, key):
                    setattr(patient, key, value)

            db.session.commit()
            return patient.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # DELETE
    @staticmethod
    def delete_patient(patient_id):
        patient = Patient.query.get(patient_id)
        if not patient:
            return False

        try:
            db.session.delete(patient)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise e

    # GET BY ID
    @staticmethod
    def get_patient_by_id(patient_id):
        patient = Patient.query.get(patient_id)
        return patient.to_dict() if patient else None

    # GET BY GENDER (sorted alphabetically)
    @staticmethod
    def get_patients_by_gender(gender):
        patients = (
            Patient.query
            .filter_by(Gender=gender)
            .order_by(Patient.LName.asc())
            .all()
        )
        return [p.to_dict() for p in patients]

    # GET ALL SORTED BY LAST NAME
    @staticmethod
    def get_all_sorted_by_lastname():
        patients = Patient.query.order_by(Patient.LName.asc()).all()
        return [p.to_dict() for p in patients]

    # OPTIONAL: GET ALL
    @staticmethod
    def get_all_patients():
        patients = Patient.query.order_by(Patient.LName.asc()).all()
        return [p.to_dict() for p in patients]
