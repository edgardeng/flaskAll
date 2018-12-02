from flask import render_template, request, current_app, flash, url_for, abort
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from .. import main
from ...models import User, Article, Follow
from ... import db

@main.route('/api/users', methods=['GET', 'POST'])
def users():
    return '1'


# show some one home page
@main.route('/user/<user_id>')
def user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
        return
    follower_count = user.follower.count()
    following_count = user.following.count()
    page = request.args.get('page', 1, type=int)
    size = current_app.config['FLASK_POSTS_PER_PAGE']
    query = Article.query
    pagination = query.filter_by(author_id=user_id).order_by(Article.created_at.desc()).paginate(page, per_page=size)
    posts = [{'author': item.author, 'created_at': item.created_at, 'body': item.body,
              'id': item.id, 'title': item.title, 'comment_count': item.comments.count()}
             for item in pagination.items]
    return render_template('user.html',
                           follower_count=follower_count, following_count=following_count,
                           user=user, articles=posts, pagination=pagination)


# show some one home page
@main.route('/user/<user_id>/follower')
def follower(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    follower_count = user.follower.count()
    following_count = user.following.count()
    page = request.args.get('page', 1, type=int)
    size = current_app.config['FLASK_FOLLOWERS_PER_PAGE']
    pagination = user.follower.paginate(
        page, per_page=size, error_out=False)
    follows = [{'user': item.following, 'created_at': item.created_at}
               for item in pagination.items]
    return render_template('followers.html', user=user,
                           follower_count=follower_count, following_count=following_count,
                           endpoint='.follower', pagination=pagination,
                           follows=follows)


@main.route('/follow/<user_id>')
@login_required
def follow(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
        return
    exist = Follow.query.filter_by(follower_id=user.id, following_id=current_user.id).first()
    if exist is None:
        follow = Follow(follower_id=user.id, following_id=current_user.id)
        db.session.add(follow)
        db.session.commit()
        flash('follow success')
    else:
        flash('you already followed before')
    return redirect(url_for('.user', user_id=user_id))


# show some one home page
@main.route('/user/<user_id>/following')
def following(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    follower_count = user.follower.count()
    following_count = user.following.count()
    page = request.args.get('page', 1, type=int)
    size = current_app.config['FLASK_FOLLOWERS_PER_PAGE']
    pagination = user.following.paginate(
        page, per_page=size, error_out=False)
    follows = [{'user': item.follower, 'created_at': item.created_at}
               for item in pagination.items]
    return render_template('followers.html', user=user,
                           follower_count=follower_count, following_count=following_count,
                           endpoint='.following', pagination=pagination,
                           follows=follows)
