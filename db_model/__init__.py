from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

from .doctor import Doctor
from .patient import Patient
from .event import Event
from .hospital import Hospital