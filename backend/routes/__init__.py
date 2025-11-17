from .gpt_route import bp as gpt_bp
from .appointment_route import bp as appointment_bp
from .bed_record_route import bp as bed_record_bp
from .bed_route import bp as bed_bp
from .doctor_route import bp as doctor_bp
from .helper_route import bp as helper_bp
from .medical_record_route import bp as medical_record_bp
from .nurse_route import bp as nurse_bp
from .patient_route import bp as patient_bp
from .room_record_route import bp as room_record_bp
from .room_route import bp as room_bp
from .staff_shift_route import bp as staff_shift_bp
from .surgery_record_route import bp as surgery_record_bp
from .ward_route import bp as ward_bp
from .department_route import bp as department_bp

def register_routes(app):
    app.register_blueprint(gpt_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(bed_record_bp)
    app.register_blueprint(bed_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(helper_bp)
    app.register_blueprint(medical_record_bp)
    app.register_blueprint(nurse_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(room_record_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(staff_shift_bp)
    app.register_blueprint(surgery_record_bp)
    app.register_blueprint(ward_bp)
    app.register_blueprint(department_bp)