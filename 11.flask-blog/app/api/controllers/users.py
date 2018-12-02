from flask import request, jsonify, abort
from .. import api
from ...models import User
from ... import db


@api.route('/users', methods=['GET'])
def users():
    all_users = User.query.all()
    return jsonify(all_users)


@api.route('/user/<user_id>', methods=['GET'])
def show(user_id):
    one_user = User.query.filter_by(id=user_id).first()
    return jsonify(one_user)


@api.route('/user', methods=['POST'])
def add():
    if not request.json or not 'username' in request.json or not 'email' in request.json:
        abort(400)
    username = request.json['username']
    email = request.json['email']
    one = User(username=username, email=email)
    one.id = db.session.add(one)
    db.session.commit()
    return jsonify(one)


@api.route('/user/<user_id>', methods=['DELETE'])
def delete(user_id):
    one = User.query.filter_by(id=user_id)
    if not one:
        abort(404)
    one.delete()
    return jsonify({'msg': 'success'})


@api.route('/user', methods=['PUT'])
def update(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        abort(404)
    if not request.json or not 'name' in request.json or not 'email' in request.json:
        abort(400)
    name = request.json['name']
    email = request.json['email']
    row = {'name': name, 'email': email}
    User.query.filter_by(id=user_id).update(row)
    return jsonify({'msg': 'success'})




