import json

from flask import jsonify
from enum import Enum, auto
from sqlalchemy.orm.base import NO_VALUE
from sqlalchemy import event
from db.database import db
from model.watermelon_model import WatermelonModel, ChangeOperationType, ChangeLog
from model.model_helper import get_changeset_json
import time


class AnimalType(Enum):
    SHEEP = auto()
    GOAT = auto()
    COW = auto()

    @staticmethod
    def list():
        return AnimalType.SHEEP.name, AnimalType.GOAT.name, AnimalType.COW.name


class Animal(WatermelonModel):
    animal_type = db.Column(db.String(255))
    earTag = db.Column(db.String(255))
    sex = db.Column(db.String(255))
    name = db.Column(db.String(255))
    countryCode = db.Column(db.String(255))
    born_at = db.Column(db.DateTime)
    farmCode = db.Column(db.String(255))
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'))

    def serialize(self):
        return str({
            'id': self.id,
            'watermelon_id': self.watermelon_id,
            'earTag': self.earTag,
            'name': self.name
        })

    def watermelon_representation(self):
        return {
            'id': self.watermelon_id,
            'animal_type': self.animal_type,
            'ear_tag': self.earTag,
            'sex': self.sex,
            'name': self.name,
            'country_code': self.countryCode,
            'farm_code': self.farmCode,
            'born_at': time.mktime(self.born_at.timetuple())
        }


class AnimalChangelog(ChangeLog):
    __tablename__ = 'animal_changelog'


@event.listens_for(Animal.name, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Animal.animal_type, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Animal.earTag, 'set')
def receive_set(target, new_value, oldvalue, initiator):
    if oldvalue is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, oldvalue, new_value)


@event.listens_for(Animal.sex, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Animal.countryCode, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Animal.farmCode, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


#@event.listens_for(Animal.born_at, 'set')
#def receive_set(target, new_value, old_value, initiator):
#    if old_value is not NO_VALUE and target.id is not None:
#        create_changelog_update_entry(target.id, initiator.key, old_value, new_value)


@event.listens_for(Animal, 'before_delete')
def receive_before_delete(mapper, connection, target: Animal):
    changelog_entry = AnimalChangelog(operation=ChangeOperationType.DELETE, watermelon_id=target.watermelon_id,
                                      old_value=str(target.serialize()))
    db.session.add(changelog_entry)


def create_changelog_update_entry(watermelon_id: str, key: str, old_value: str, new_value: str):
    changelog_entry = AnimalChangelog(operation=ChangeOperationType.UPDATE, watermelon_id=watermelon_id,
                                      old_value=get_changeset_json(key, old_value, new_value))
    db.session.add(changelog_entry)
