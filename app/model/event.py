from enum import Enum, auto
from sqlalchemy.orm.base import NO_VALUE
from sqlalchemy import event
from app.db.database import db
from app.model.watermelon_model import WatermelonModel, ChangeOperationType, ChangeLog
from app.model.model_helper import get_changeset_json, get_epoch_from_datetime, get_datetime_from_epoch
import datetime

class Event(WatermelonModel):
    type = db.Column(db.String(255))
    animal_id = db.Column(db.String(255))
    description = db.Column(db.String(255))
    model_created_at = db.Column(db.DateTime)

    def serialize(self):
        return str({
            'id': self.id,
            'watermelon_id': self.watermelon_id,
            'type': self.type,
            'animal_id': self.animal_id,
            'description': self.description,
            'created_at': self.model_created_at
        })

    def watermelon_representation(self, migration_number: int):
        object_11 = {
            'id': self.watermelon_id,
            'event_type': self.type,
            'animal_id': self.animal_id,
            'description': self.description,
            'created_at': get_epoch_from_datetime(self.model_created_at)
        }
        return object_11

    @staticmethod
    def create_from_json(object_json, farm_id, last_pulled_at, migration_number: int = 11):
        animal = Event(object_json=object_json, farm_id=farm_id, last_pulled_at=last_pulled_at)
        animal.model_created_at = get_datetime_from_epoch(object_json['created_at'])
        animal.animal_id = object_json['animal_id']
        animal.type = object_json['event_type']
        animal.description = object_json['description']
        return animal

    def update_from_json(self, update_json, migration_number: int = 11, last_pulled_at=datetime.now()):
        WatermelonModel.update_from_json(self, update_json, migration_number, last_pulled_at)

        if self.model_created_at != get_datetime_from_epoch(update_json['created_at']):
            self.model_created_at = get_datetime_from_epoch(update_json['created_at'])
        if self.type != update_json['event_type']:
            self.type = update_json['event_type']
        if self.animal_id != update_json['animal_id']:
            self.animal_id = update_json['animal_id']
        if self.description != update_json['description']:
            self.description = update_json['description']


class EventChangelog(ChangeLog):
    __tablename__ = 'event_changelog'


@event.listens_for(Event.description, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.id, initiator.key, str(old_value), str(new_value))


@event.listens_for(Event.model_created_at, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.id, initiator.key, str(old_value), str(new_value))


@event.listens_for(Event.type, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Event.animal_id, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Event, 'before_delete')
def receive_before_delete(mapper, connection, target: Event):
    changelog_entry = EventChangelog(operation=ChangeOperationType.DELETE, watermelon_id=target.watermelon_id,
                                     old_value=str(target.serialize()))
    db.session.add(changelog_entry)


def create_changelog_update_entry(watermelon_id: str, key: str, old_value: str, new_value: str):
    changelog_entry = EventChangelog(operation=ChangeOperationType.UPDATE, watermelon_id=watermelon_id,
                                     old_value=get_changeset_json(key, old_value, new_value))
    db.session.add(changelog_entry)
