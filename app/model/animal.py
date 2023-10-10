from enum import Enum, auto
from sqlalchemy.orm.base import NO_VALUE
from sqlalchemy import event
from app.db.database import db
from app.model.watermelon_model import WatermelonModel, ChangeOperationType, ChangeLog
from app.model.model_helper import get_changeset_json
import time
from datetime import datetime


class AnimalType(Enum):
    SHEEP = auto()
    GOAT = auto()
    COW = auto()

    @staticmethod
    def list():
        return AnimalType.SHEEP.name, AnimalType.GOAT.name, AnimalType.COW.name


class Animal(WatermelonModel):
    animal_type = db.Column(db.String(255))
    ear_tag = db.Column(db.String(255))
    sex = db.Column(db.String(255))
    name = db.Column(db.String(255))
    country_code = db.Column(db.String(255))
    born_at = db.Column(db.DateTime)
    farm_code = db.Column(db.String(255))
    description = db.Column(db.Text())

    def serialize(self):
        return str({
            'id': self.id,
            'watermelon_id': self.watermelon_id,
            'ear_tag': self.ear_tag,
            'name': self.name
        })

    def watermelon_representation(self, migration_number: int):
        object_11 = {
            'id': self.watermelon_id,
            'animal_type': self.animal_type,
            'ear_tag': self.ear_tag,
            'sex': self.sex,
            'name': self.name,
            'country_code': self.country_code,
            'farm_code': self.farm_code,
            'born_at': time.mktime(self.born_at.timetuple())
        }
        if migration_number > 11:
            object_11 = object_11 | {'description': self.description}
        return object_11

    @staticmethod
    def create_from_json(object_json, farm_id):
        return Animal(watermelon_id=object_json['id'], sex=object_json['sex'], animal_type=object_json['animal_type'],
                      ear_tag=object_json['ear_tag'], born_at=datetime.fromtimestamp(object_json['born_at'] / 1000),
                      farm_code=object_json['farm_code'], country_code=object_json['country_code'],
                      name=object_json['name'], description=object_json['description'], farm_id=farm_id)

    def update_from_json(self, animal_json):
        if self.sex != animal_json['sex']:
            self.sex = animal_json['sex']
        if self.animal_type != animal_json['animal_type']:
            self.animal_type = animal_json['animal_type']
        if self.ear_tag != animal_json['ear_tag']:
            self.ear_tag = animal_json['ear_tag']
        if self.born_at != datetime.fromtimestamp(animal_json['born_at'] / 1000):
            self.born_at = datetime.fromtimestamp(animal_json['born_at'] / 1000)
        if self.country_code != animal_json['country_code']:
            self.country_code = animal_json['country_code']
        if self.farm_code != animal_json['farm_code']:
            self.farm_code = animal_json['farm_code']
        if self.name != animal_json['name']:
            self.name = animal_json['name']
        if self.description != animal_json['description']:
            self.description = animal_json['description']


class AnimalChangelog(ChangeLog):
    __tablename__ = 'animal_changelog'


@event.listens_for(Animal.name, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Animal.description, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Animal.animal_type, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Animal.ear_tag, 'set')
def receive_set(target, new_value, oldvalue, initiator):
    if oldvalue is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, oldvalue, new_value)


@event.listens_for(Animal.sex, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Animal.country_code, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Animal.farm_code, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Animal.born_at, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.id, initiator.key, str(old_value), str(new_value))


@event.listens_for(Animal, 'before_delete')
def receive_before_delete(mapper, connection, target: Animal):
    changelog_entry = AnimalChangelog(operation=ChangeOperationType.DELETE, watermelon_id=target.watermelon_id,
                                      old_value=str(target.serialize()))
    db.session.add(changelog_entry)


def create_changelog_update_entry(watermelon_id: str, key: str, old_value: str, new_value: str):
    changelog_entry = AnimalChangelog(operation=ChangeOperationType.UPDATE, watermelon_id=watermelon_id,
                                      old_value=get_changeset_json(key, old_value, new_value))
    db.session.add(changelog_entry)
