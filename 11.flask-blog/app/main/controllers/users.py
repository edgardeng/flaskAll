from flask import render_template, request, current_app
from flask_login import current_user
from .. import main
from ...models import User, Article


@main.route('/api/users', methods=['GET', 'POST'])
def users():
    return '1'


# show some one home page
@main.route('/user/<user_id>')
def user(user_id):
    one_user = User.query.filter_by(id=user_id).first()
    page = request.args.get('page', 1, type=int)
    size = current_app.config['FLASK_POSTS_PER_PAGE']
    query = Article.query
    is_author = current_user.id == one_user.id
    pagination = query.filter_by(author_id=user_id).order_by(Article.created_at.desc()).paginate(page, per_page=size)
    posts = pagination.items
    # print(posts)
    return render_template('user.html', user=one_user, articles=posts, pagination=pagination,is_author=is_author)


# show some one home page
@main.route('/user/<user_id>/followed')
def followed(user_id):
    one_user = User.query.filter_by(id=user_id).first()
    page = request.args.get('page', 1, type=int)
    # query = Article.query.filter_by(author_id=id)
    size = current_app.config['FLASK_POSTS_PER_PAGE']
    query = Article.query  # .filter_by(author_id=user_id).all()
    pagination = query.filter_by(author_id=user_id).order_by(Article.created_at.desc()).paginate(page, per_page=size)
    posts = pagination.items
    # print(posts)
    return render_template('user.html', user=one_user, articles=posts, pagination=pagination)


# show some one home page
@main.route('/user/<user_id>/following')
def following(user_id):
    one_user = User.query.filter_by(id=user_id).first()
    page = request.args.get('page', 1, type=int)
    # query = Article.query.filter_by(author_id=id)
    size = current_app.config['FLASK_POSTS_PER_PAGE']
    query = Article.query  # .filter_by(author_id=user_id).all()
    pagination = query.filter_by(author_id=user_id).order_by(Article.created_at.desc()).paginate(page, per_page=size)
    posts = pagination.items
    # print(posts)
    return render_template('user.html', user=one_user, articles=posts, pagination=pagination)
