from db_model import db, Appointment
from datetime import datetime

class AppointmentService:

    # CREATE
    @staticmethod
    def create_appointment(data):
        """Create a new appointment. Allow user-defined appointment_Id if provided."""
        try:
            # Safety check: If user provides an ID, ensure no collision.
            custom_id = data.get("appoIntment_Id")
            if custom_id is not None:
                existing = Appointment.query.get(custom_id)
                if existing:
                    raise ValueError(f"Appointment ID {custom_id} already exists.")

            new_appointment = Appointment(
                appoIntment_Id=custom_id,       # Only set if user provides it
                patient_Id=data.get("patient_Id"),
                doct_Id=data.get("doct_Id"),
                reason=data.get("reason"),
                appointment_Date=data.get("appointment_Date"),
                payment_amount=data.get("payment_amount"),
                mode_of_payment=data.get("mode_of_payment"),
                mode_of_appointment=data.get("mode_of_appointment"),
                appointment_status=data.get("appointment_status", "Scheduled")
            )

            db.session.add(new_appointment)
            db.session.commit()
            return new_appointment.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e


    # UPDATE
    @staticmethod
    def update_appointment(appointment_id, data):
        """Update an existing appointment."""
        appointment = Appointment.query.get(appointment_id)

        if not appointment:
            return None

        try:
            for key, value in data.items():
                if hasattr(appointment, key):
                    setattr(appointment, key, value)

            db.session.commit()
            return appointment.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # GET BY ID
    @staticmethod
    def get_appointment_by_id(appointment_id):
        """Retrieve appointment by primary key."""
        appointment = Appointment.query.get(appointment_id)
        return appointment.to_dict() if appointment else None

    # GET BY PATIENT
    @staticmethod
    def get_appointments_by_patient(patient_id):
        """Retrieve all appointments for a given patient."""
        appointments = Appointment.query.filter_by(patient_Id=patient_id).all()
        return [appt.to_dict() for appt in appointments]

    # GET BY DOCTOR
    @staticmethod
    def get_appointments_by_doctor(doctor_id):
        """Retrieve all appointments for a given doctor."""
        appointments = Appointment.query.filter_by(doct_Id=doctor_id).all()
        return [appt.to_dict() for appt in appointments]

    # GET ALL
    @staticmethod
    def get_all_appointments():
        """Retrieve all appointments in the database."""
        appointments = Appointment.query.all()
        return [appt.to_dict() for appt in appointments]

    # DELETE
    @staticmethod
    def delete_appointment(appointment_id):
        """Delete an appointment by id."""
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return False

        try:
            db.session.delete(appointment)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise e
