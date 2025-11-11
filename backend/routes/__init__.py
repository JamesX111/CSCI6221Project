from .event_route import bp as event_bp
from .hospital_route import bp as hospital_bp
from .patient_route import bp as patient_bp
from .gpt_route import bp as gpt_bp
from .accident_route import bp as accident_bp

def register_routes(app):
    app.register_blueprint(event_bp)
    app.register_blueprint(hospital_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(accident_bp)
    app.register_blueprint(gpt_bp)
