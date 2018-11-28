from flask import Blueprint

main = Blueprint('main', __name__)


from ..models import Permission
# add controllers
from .controllers import errors, users, articles


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
