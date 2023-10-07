import uuid
from datetime import datetime
from enum import Enum, auto
from db.database import db


class ChangeOperationType(Enum):
    CREATE = auto()
    UPDATE = auto()
    DELETE = auto()


class WatermelonModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    watermelon_id = db.Column(db.String(255))
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_changed_at = db.Column(db.DateTime, default=datetime.now)


class ChangeLog(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    timestamp_at = db.Column(db.DateTime, default=datetime.now)
    operation = db.Column(db.Enum(ChangeOperationType), nullable=False)
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'))
