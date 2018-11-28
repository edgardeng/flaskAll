from flask import render_template, request, current_app, make_response
from .. import main
from ...models import User, Article


@main.route('/api/users', methods=['GET', 'POST'])
def users():
    return '1'


@main.route('/user/<user_id>')
def user(user_id):
    one_user = User.query.filter_by(id=user_id).first()
    page = request.args.get('page', 1, type=int)
    # query = Article.query.filter_by(author_id=id)
    size = current_app.config['FLASK_POSTS_PER_PAGE']
    query = Article.query  # .filter_by(author_id=user_id).all()
    pagination = query.filter_by(author_id=user_id).order_by(Article.created_at.desc()).paginate(page, per_page=size)
    posts = pagination.items
    # print(posts)
    return render_template('user.html', user=one_user, articles=posts, pagination=pagination)
