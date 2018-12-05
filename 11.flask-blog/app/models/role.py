from .. import db
from datetime import datetime


class Role(db.Model):
    __tablename__ = 't_role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    is_default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)  # 1 USER 2 ADMIN
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    users = db.relationship('User', backref='role', lazy='dynamic')


    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return '<Role %r>' % self.name