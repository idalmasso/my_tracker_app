from flask import Blueprint

bp = Blueprint('trackerapp', __name__)

from app.trackerapp import routes
