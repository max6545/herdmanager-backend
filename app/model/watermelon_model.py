import uuid
from datetime import datetime
from uuid import UUID

from db.database import db


class WatermelonModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    watermelon_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_changed_at = db.Column(db.DateTime, default=datetime.now)
