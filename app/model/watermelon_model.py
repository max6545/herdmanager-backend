from datetime import datetime
from enum import Enum, auto
from app.db.database import db


class ChangeOperationType(Enum):
    CREATE = auto()
    UPDATE = auto()
    DELETE = auto()


class WatermelonModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    watermelon_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_changed_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    farm_id = db.Column(db.Integer())

    def watermelon_representation(self, migration_number: int):
        raise NotImplementedError
    @staticmethod
    def create_from_json(object_json, farm_id):
        raise NotImplementedError

    def update_from_json(self, update_json):
        raise NotImplementedError


class ChangeLog(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    watermelon_id = db.Column(db.String(255))
    farm_id = db.Column(db.Integer())
    action_at = db.Column(db.DateTime, default=datetime.now)
    operation = db.Column(db.Enum(ChangeOperationType), nullable=False)
    old_value = db.Column(db.Text())

    def serialize(self):
        return {
            'id': self.id,
            'watermelon_id': self.watermelon_id,
            'farm_id': self.farm_id,
            'operation': self.operation,
            'action_at': self.action_at,
            'old_value': self.old_value
        }
