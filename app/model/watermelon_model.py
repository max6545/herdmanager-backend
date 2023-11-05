from datetime import datetime
from enum import Enum, auto
from app.db.database import db
from app.model.model_helper import get_datetime_from_epoch


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

    def serialize(self):
        return str({
            'id': self.id,
            'watermelon_id': self.watermelon_id,
            'name': self.name
        })

    def __init__(self, object_json, farm_id, last_pulled_at):
        self.watermelon_id = object_json['id']
        self.farm_id = farm_id
        self.created_at = last_pulled_at
        self.last_changed_at = last_pulled_at
        for element in self.__table__.c:
            if (element.key not in ['id', 'watermelon_id', 'farm_id', 'created_at', 'last_changed_at']
                    and object_json[element.key]):
                if element.type.__class__.__name__ in ['Integer', 'String', 'Text']:
                    setattr(self, element.key, object_json[element.key])
                if element.type.__class__.__name__ == 'DateTime':
                    setattr(self, element.key, get_datetime_from_epoch(object_json[element.key]))

    def watermelon_representation(self, migration_number: int):
        raise NotImplementedError

    def update_from_json(self, update_json, migration_number: int = 11, last_pulled_at=datetime.now()):
        changed_fields = str(update_json['_changed']).split(',')
        for element in self.__table__.c:
            if element.key in changed_fields and update_json[element.key]:
                if element.type.__class__.__name__ in ['Integer', 'String', 'Text']:
                    setattr(self, element.key, update_json[element.key])
                if element.type.__class__.__name__ == 'DateTime':
                    setattr(self, element.key, get_datetime_from_epoch(update_json[element.key]))


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
