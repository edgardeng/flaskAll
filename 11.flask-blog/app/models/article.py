from .. import db
# from .user import User
# from .comment import Comment

from datetime import datetime
from markdown import markdown
import bleach


class Article(db.Model):
    __tablename__ = 't_article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('t_user.id'))
    comments = db.relationship('Comment', backref='article', lazy='dynamic')
    # author = db.relationship('User', backref='author', uselist=False)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        html_body = markdown(value, output_format='html')
        html_body = bleach.clean(html_body, tags=allowed_tags, strip=True)
        html_body = bleach.linkify(html_body)
        target.html_body = html_body
        # target.body_html = bleach.linkify(bleach.clean(
        #     markdown(value, output_format='html'),
        #     tags=allowed_tags, strip=True))


db.event.listen(Article.body, 'set', Article.on_changed_body)
