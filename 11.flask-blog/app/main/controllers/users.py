from flask import render_template, request, current_app, flash, url_for, abort
from flask_login import current_user, login_required

from werkzeug.utils import redirect

from ..decorators import admin_required
from .. import main
from ...models import User, Article, Follow
from ... import db


@main.route('/users')
@login_required
@admin_required
def users():
    query = User.query.all()
    return render_template('users.html', users=query)


@main.route('/user/<user_id>/role')
@admin_required
def set_role(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
        return
    user.change_role()
    return redirect(url_for('.users'))


# show some one home page
@main.route('/user/<user_id>')
def user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
        return
    page = request.args.get('page', 1, type=int)
    size = current_app.config['FLASK_POSTS_PER_PAGE']
    is_author = current_user.get_id() == user_id
    if is_author:
        query = Article.query.filter_by(author_id=user_id)
    else:
        query = Article.query.filter_by(author_id=user_id, is_forbidden=0)
    pagination = query.order_by(Article.created_at.desc()).paginate(page, per_page=size)
    posts = pagination.items
    return render_template('user.html', is_author=is_author,
                           user=user, articles=posts, pagination=pagination)


# show some one home page
@main.route('/user/<user_id>/follower')
def follower(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    size = current_app.config['FLASK_FOLLOWERS_PER_PAGE']
    pagination = user.follower.paginate(
        page, per_page=size, error_out=False)
    follows = [{'user': item.following, 'created_at': item.created_at}
               for item in pagination.items]
    return render_template('followers.html', user=user,
                           endpoint='.follower', pagination=pagination,
                           follows=follows)


# follow some one
@main.route('/follow/<user_id>')
@login_required
def follow(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
        return
    exist = Follow.query.filter_by(follower_id=user.id, following_id=current_user.id)
    if exist.first() is None:
        follow = Follow(follower_id=user.id, following_id=current_user.id)
        db.session.add(follow)
        flash('follow success')
    else:
        exist.delete()
        flash('not follow already')
    db.session.commit()
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
