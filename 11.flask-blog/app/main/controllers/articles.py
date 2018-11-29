from flask import render_template, request, current_app, flash, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from .. import main
from ...models import Article, Permission
from ..forms import PostForm
from ... import db


# show all article in index page
@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    # show_followed = False
    # if current_user.is_authenticated:
    #     print('is_authenticated')
    #     show_followed = bool(request.cookies.get('show_followed', ''))
    query = Article.query
    size = current_app.config['FLASK_POSTS_PER_PAGE'];

    pagination = query.order_by(Article.created_at.desc()).paginate(page, per_page=size, error_out=True)
    posts = pagination.items
    return render_template('index.html', articles=posts, pagination=pagination)


@main.route('/about')
def about():
    return render_template('about.html')


# show some one home page

# show article page


@main.route('/article/<id>')
def article(id):
    one_article = Article.query.get_or_404(id)
    page = 1
    size = current_app.config['FLASK_COMMENTS_PER_PAGE']
    pagination = one_article.comments.paginate(
        page, per_page=size, error_out=False)
    is_author = current_user == one_article.author
    comments = pagination.items
    return render_template('post.html', post=one_article, comments=comments, is_author=is_author)


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
        # TODO add author id
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.article', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)
