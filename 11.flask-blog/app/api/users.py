from flask import request, jsonify, url_for, current_app, abort
from . import api
from .. models import User, Article
from .. import db
from .authentication import auth
from .decorators import admin_required


@api.route('/user', methods=['GET'])
@auth.login_required
@admin_required
def list():
    all_users = User.query.all()
    return jsonify(User.to_json_list(all_users))


@api.route('/user/<user_id>', methods=['GET'])
def show(user_id):
    one_user = User.query.filter_by(id=user_id).first()
    return jsonify(one_user.to_json())


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
    return jsonify(one.to_json())


@auth.login_required
@api.route('/user/<user_id>', methods=['DELETE'])
def delete(user_id):
    one = User.query.filter_by(id=user_id)
    if not one:
        abort(404)
    one.delete()
    db.session.commit()
    return jsonify({'msg': 'success'})


@auth.login_required
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


@api.route('/users/<int:id>/article')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    size = current_app.config['FLASK_POSTS_PER_PAGE']
    pagination = user.posts.order_by(Article.created_at.desc()).paginate(
        page, per_page=size, error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_posts', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_posts', id=id, page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
})
