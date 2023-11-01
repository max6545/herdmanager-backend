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
    last_changed_at = db.Column(db.DateTime, default=datetime.now)
    farm_id = db.Column(db.Integer())

    def __init__(self, object_json, farm_id, last_pulled_at):
        self.watermelon_id = object_json['id']
        self.farm_id = farm_id
        self.created_at = last_pulled_at
        self.last_changed_at = last_pulled_at

    def watermelon_representation(self, migration_number: int):
        raise NotImplementedError

    @staticmethod
    def create_from_json(object_json, farm_id, migration_number: int = 11):
        raise NotImplementedError

    def update_from_json(self, update_json, migration_number: int = 11, last_pulled_at=datetime.now()):
        self.last_changed_at = last_pulled_at



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
