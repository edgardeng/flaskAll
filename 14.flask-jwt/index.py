# example for flask-jwt

from flask import Flask, render_template, request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id


users = [
    User(1, 'user1', '123456'),
    User(2, 'user2', '123456'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


# add by edgardeng
@app.route('/')
def index():
    name = ''
    access_token = request.args.get('access_token')
    if access_token:
        payload = jwt.jwt_decode_callback(access_token)
        user = identity(payload)
        name = user.username
        print(access_token)
        print(payload)
    if len(name) > 0:
        return render_template('index.html', name=name)
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run()
