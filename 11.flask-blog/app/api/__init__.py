from flask import Blueprint

api = Blueprint('api', __name__)

from .controllers import users, articles
