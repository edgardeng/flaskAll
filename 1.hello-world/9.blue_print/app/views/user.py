from flask import Blueprint

ur = Blueprint('user', __name__)

@ur.route('/a')
def view_a():
    return "view_user_a"

@ur.route('/b')
def view_b():
    return "view_user_b"
