# example for flask with pyjwt


from flask import Flask, request, jsonify, render_template
import time
import jwt
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


def identity(token):
    key = app.config['SECRET_KEY']
    payload = jwt.decode(token, key, algorithms='HS256')
    print(payload)
    user_id = payload['identity']
    return userid_table.get(user_id, None)


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'


def create_access_token(identity):
    key = app.config['SECRET_KEY']
    utcnow = int(time.time())
    expire = utcnow + 1000 * 120
    encoded = jwt.encode({'identity': identity, 'exp': expire, 'iat': utcnow}, key, algorithm='HS256')
    token = str(encoded, encoding='utf-8')
    return token


@app.route('/auth', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    user = authenticate(username, password)
    if not user:
        return jsonify({"msg": "Bad username or password"}), 401
    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200


@app.route('/protected', methods=['GET'])
def protected():
    auth = request.authorization
    print(auth)
    return jsonify(logged_in_as='a'), 200


# add by edgardeng
@app.route('/')
def index():
    name = ''
    access_token = request.args.get('access_token')
    if access_token:
        user = identity(access_token)
        name = user.username
        print(access_token)
    if len(name) > 0:
        return render_template('index.html', name=name)
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run()
