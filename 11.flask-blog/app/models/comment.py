from .. import db
from datetime import datetime


class Comment(db.Model):
    __tablename__ = 't_comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('t_user.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('t_article.id'))
