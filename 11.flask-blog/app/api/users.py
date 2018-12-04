from flask import request, jsonify, abort
from . import api
from .. models import User
from .. import db


@api.route('/', methods=['GET'])
def api_index():
    index = {'url': '/api/', 'name': 'flask-blog', 'version': '1.0'}
    return jsonify(index)


@api.route('/user', methods=['GET'])
def list():
    all_users = User.query.all()
    return jsonify(User.as_dict_list(all_users))


@api.route('/user/<user_id>', methods=['GET'])
def show(user_id):
    one_user = User.query.filter_by(id=user_id).first()
    return jsonify(one_user.as_dict())


@api.route('/user', methods=['POST'])
def add():
    json = request.json
    if not json or not 'password' in json or not 'username' in json or not 'email' in json:
        abort(400)
    username = json['username']
    email = json['email']
    password = json['password']
    one = User(username=username, email=email, password=password)
    one.id = db.session.add(one)
    db.session.commit()
    return jsonify(one.as_dict())


@api.route('/user/<user_id>', methods=['DELETE'])
def delete(user_id):
    one = User.query.filter_by(id=user_id)
    if not one:
        abort(404)
    one.delete()
    db.session.commit()
    return jsonify({'msg': 'success'})


@api.route('/user/<user_id>', methods=['PUT'])
def update(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        abort(404)
    if not request.json or not 'username' in request.json or not 'email' in request.json:
        abort(400)
    name = request.json['username']
    email = request.json['email']
    row = {'username': name, 'email': email}
    User.query.filter_by(id=user_id).update(row)
    return jsonify({'msg': 'success'})
