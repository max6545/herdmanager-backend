from db.database import db
from datetime import datetime


class MobileDevice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    added_at = db.Column(db.DateTime, default=datetime.now())
    last_pull_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))