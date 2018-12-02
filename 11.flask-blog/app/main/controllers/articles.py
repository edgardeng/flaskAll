from flask import render_template, request, current_app, flash, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from .. import main
from ...models import Article, Permission, Comment
from ..forms import PostForm, CommentForm
from ... import db


# show all article in index page
@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    query = Article.query
    size = current_app.config['FLASK_POSTS_PER_PAGE'];
    pagination = query.order_by(Article.created_at.desc()).paginate(page, per_page=size, error_out=True)
    # posts = pagination.items
    posts = [{'author': item.author, 'created_at': item.created_at, 'body': item.body,
              'id': item.id, 'title': item.title, 'comment_count': item.comments.count()}
               for item in pagination.items]
    return render_template('index.html', articles=posts, pagination=pagination)


@main.route('/about')
def about():
    return render_template('about.html')


# article page & add comment
@main.route('/article/<id>', methods=['GET', 'POST'])
def article(id):
    one_article = Article.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            return redirect('/auth/login?next=/article/'+id)
        author = current_user._get_current_object()
        comment = Comment(body=form.body.data,
                          article_id=id,
                          author_id=author.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('.article', id=id))
    page = request.args.get('page', 1, type=int)
    size = current_app.config['FLASK_COMMENTS_PER_PAGE']
    pagination = one_article.comments.paginate(
        page, per_page=size, error_out=False)
    is_author = current_user == one_article.author
    comments = pagination.items
    return render_template('post.html', post=one_article, comments=comments, pagination=pagination, form=form)


# article edit
@main.route('/article/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def article_edit(id):
    if id != 0:
        post = Article.query.get_or_404(id)
        if current_user != post.author and not current_user.can(Permission.ADMIN):
            abort(403)
    else:
        post = Article()
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        post.title = form.title.data
        if id == 0:
            post.author_id = current_user.id
            db.session.add(post)
            db.session.commit()  # add article
            flash('The new post has been added !')
        else:
            row = {'title': post.title, 'body': post.body}
            db.session.query(Article).filter_by(id=id).update(row)
            db.session.commit()
            flash('The post has been updated !')
        return redirect(url_for('.article', id=post.id))
    form.body.data = post.body
    form.title.data = post.title
    return render_template('edit_post.html', form=form, id=id)


@main.route('/article/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def article_delete(id):
    query = Article.query.filter_by(id=id)
    post = query.first()
    if not post:
        abort(404)
    if current_user != post.author and not current_user.can(Permission.ADMIN):
        abort(403)
    db.session.query(Comment).filter_by(article_id=id).delete()
    query.delete()
    db.session.commit()
    flash('The post has been deleted !')
    return redirect(url_for('.user', user_id=post.author_id))


@main.route('/comment/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def comment_delete(id):
    query = Comment.query.filter_by(id=id)
    comment = query.first()
    if not comment:
        abort(404)
    if current_user != comment.author and not current_user.can(Permission.ADMIN):
        abort(403)
    query.delete()
    db.session.commit()
    flash('The Comments has been deleted !')
    return redirect(url_for('.article', id=comment.article_id))
