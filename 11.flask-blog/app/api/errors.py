from flask import jsonify
from . import api
from ..exceptions import ValidationError


@api.app_errorhandler(403)
def forbidden(e):
    response = jsonify({'error': 'forbidden'})
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


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e)