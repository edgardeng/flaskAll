from flask import g, jsonify, request, session
from flask_httpauth import HTTPTokenAuth
from ..models import User
from . import api
from .errors import unauthorized

# init auth
# auth = HTTPBasicAuth('Bearer')
auth = HTTPTokenAuth('Bearer')


def verify_password(email_or_token, password):
    if not email_or_token or email_or_token == '':
        return False
    if not password:
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@auth.verify_token
def verify_token(email_or_token):
    return verify_password(email_or_token, None)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.before_request
def before_request():
    # may be g.current_user == None
    pass
    # if not g.current_user.is_anonymous and not g.current_user.confirmed:
    #     return forbidden('Unconfirmed account')


@api.route('/login', methods=['POST'])
def login():
    if not request.json or not 'email' in request.json or not 'password' in request.json:
        return jsonify({'message': 'empty username or password'})
    email = request.json['email']
    password = request.json['password']
    if verify_password(email, password):
        token = g.current_user.generate_auth_token(300)
        session['token'] = token
        return jsonify({'token': token, 'expiration': 300})
    return jsonify({'message': 'error username or password'})


@api.route('/token', methods=['POST'])
@auth.login_required
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(expiration=300), 'expiration': 300})
