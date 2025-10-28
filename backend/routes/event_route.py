
from flask import Blueprint, request, jsonify
from datetime import datetime


bp = Blueprint('events', __name__, url_prefix='/api/events')