from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .db_model import db, init_db
app = Flask(__name__)

# Set your database URI here
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://user:password@localhost/dbname'

# Optional: disable track modifications (to avoid warning)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


