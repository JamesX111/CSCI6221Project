# ===============================================================
# db_model/__init__.py
# ---------------------------------------------------------------
# Centralized database initialization and model exposure
# ===============================================================

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# IMPORT ALL MODELS SO SQLALCHEMY REGISTERS THEM
# The order matters when relationships exist.
from .patient import Patient
from .doctor import Doctor
from .hospital import Hospital
from .event import Event
from .bed_occupancy import BedOccupancy



# def init_db(app):
#     """Initialize SQLAlchemy and create all tables."""
#     db.init_app(app)
#     with app.app_context():
#         # Import models so SQLAlchemy recognizes them before create_all()
#         from .patient import Patient
#         from .doctor import Doctor
#         from .hospital import Hospital
#         from .event import Event
#         from .bed_occupancy import BedOccupancy

#         db.create_all()

# Expose models at package level
# from .patient import Patient
# from .doctor import Doctor
# from .hospital import Hospital
# from .event import Event
# from .bed_occupancy import BedOccupancy
