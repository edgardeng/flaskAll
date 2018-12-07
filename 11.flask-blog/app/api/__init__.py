from flask import Blueprint

api = Blueprint('api', __name__)

from . import errors, users, articles
# add auth
from . import authentication