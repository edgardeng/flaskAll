from .. import db
from datetime import datetime


class Follow(db.Model):
    __tablename__ = 't_follow'
    follower_id = db.Column(db.Integer, db.ForeignKey('t_user.id'), primary_key=True)
    following_id = db.Column(db.Integer, db.ForeignKey('t_user.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
