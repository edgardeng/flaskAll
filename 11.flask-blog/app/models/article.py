from .. import db
from datetime import datetime
from markdown import markdown
import bleach
from ..exceptions import ValidationError


class Article(db.Model):
    __tablename__ = 't_article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    is_forbidden = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('t_user.id'))
    comments = db.relationship('Comment', backref='article', lazy='dynamic')

    @staticmethod
    def from_json(json_post):
        if not json_post:
            raise ValidationError('post does not have a body')
        title = json_post.get('title')
        body = json_post.get('body')
        if body is None or body == '' or title is None:
            raise ValidationError('post does not have a body')
        return Article(title=title, body=body)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def comment_count(self):
        return self.comments.count()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        html_body = markdown(value, output_format='html')
        html_body = bleach.clean(html_body, tags=allowed_tags, strip=True)
        html_body = bleach.linkify(html_body)
        target.html_body = html_body
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(Article.body, 'set', Article.on_changed_body)
