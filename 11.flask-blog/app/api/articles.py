from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Article
from . import api
from .errors import forbidden
from .authentication import auth


@api.route('/article')
def get_posts():
    page = request.args.get('page', 1, type=int)
    size = current_app.config['FLASK_POSTS_PER_PAGE']
    pagination = Article.query.paginate(
        page, per_page=size, error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/article/<int:id>')
def get_post(id):
    post = Article.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/article', methods=['POST'])
@auth.login_required
def new_post():
    post = Article.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, {'Location': url_for('api.get_post', id=post.id)}


@api.route('/article/<int:id>', methods=['PUT'])
@auth.login_required
def edit_post(id):
    post = Article.query.get_or_404(id)
    if g.current_user != post.author and not g.current_user.is_administrator():
        return forbidden('Insufficient permissions')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json())
