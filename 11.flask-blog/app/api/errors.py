from flask import jsonify
from . import api


@api.app_errorhandler(403)
def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


@api.app_errorhandler(400)
def bad_request(e):
    response = jsonify({'error': 'Bad Request'})
    response.status_code = 400
    return response


@api.app_errorhandler(405)
def bad_method(e):
    response = jsonify({'error': 'Method Not Allowed'})
    response.status_code = 405
    return response

