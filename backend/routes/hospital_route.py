
from flask import Blueprint, request, jsonify
from datetime import datetime


bp = Blueprint('hospital', __name__, url_prefix='/api/hospital')