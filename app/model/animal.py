from enum import Enum, auto
from sqlalchemy.orm.base import NO_VALUE
from sqlalchemy import event
from app.db.database import db
from app.model.watermelon_model import WatermelonModel, ChangeOperationType, ChangeLog
from app.model.model_helper import get_changeset_json, get_epoch_from_datetime, get_datetime_from_epoch
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
    rejected_at = db.Column(db.DateTime)
    rejected_reason = db.Column(db.Text())
    rejected_info = db.Column(db.Text())
    lot_id = db.Column(db.Text())
    father_id = db.Column(db.Text())
    mother_id = db.Column(db.Text())

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
            'born_at': get_epoch_from_datetime(self.born_at),
            'father_id': self.father_id,
            'mother_id': self.mother_id,

        }
        if migration_number > 11:
            object_11 = object_11 | {'description': self.description}
        if migration_number > 12:
            object_11 = object_11 | {'rejected_at': get_epoch_from_datetime(self.rejected_at),
                                     'rejected_reason': self.rejected_reason,
                                     'rejected_info': self.rejected_info,
                                     'lot_id': self.lot_id,
                                     'father_id': self.father_id,
                                     'mother_id': self.mother_id}
        return object_11

    @staticmethod
    def create_from_json(object_json, farm_id, last_pulled_at, migration_number: int = 11):
        animal = Animal(object_json=object_json, farm_id=farm_id, last_pulled_at=last_pulled_at)
        animal.sex = object_json['sex']
        animal.animal_type = object_json['animal_type']
        animal.ear_tag = object_json['ear_tag']
        animal.born_at = get_datetime_from_epoch(object_json['born_at'])
        animal.farm_code = object_json['farm_code']
        animal.country_code = object_json['country_code']
        animal.name = object_json['name']
        animal.description = object_json['description']
        animal.rejected_at = get_datetime_from_epoch(object_json['rejected_at'])
        animal.rejected_reason = object_json['rejected_reason']
        animal.rejected_info = object_json['rejected_info']
        animal.lot_id = object_json['lot_id']
        animal.father_id = object_json['father_id']
        animal.mother_id = object_json['mother_id']
        return animal

    def update_from_json(self, update_json, migration_number: int = 11, last_pulled_at=datetime.now()):
        WatermelonModel.update_from_json(self, update_json, migration_number, last_pulled_at)
        if self.sex != update_json['sex']:
            self.sex = update_json['sex']
        if self.animal_type != update_json['animal_type']:
            self.animal_type = update_json['animal_type']
        if self.ear_tag != update_json['ear_tag']:
            self.ear_tag = update_json['ear_tag']
        if self.born_at != get_datetime_from_epoch(update_json['born_at']):
            self.born_at = get_datetime_from_epoch(update_json['born_at'])
        if self.country_code != update_json['country_code']:
            self.country_code = update_json['country_code']
        if self.farm_code != update_json['farm_code']:
            self.farm_code = update_json['farm_code']
        if self.name != update_json['name']:
            self.name = update_json['name']
        if self.description != update_json['description']:
            self.description = update_json['description']
        if self.rejected_at != get_datetime_from_epoch(update_json['rejected_at']):
            self.rejected_at = get_datetime_from_epoch(update_json['rejected_at'])
        if self.rejected_reason != update_json['rejected_reason']:
            self.rejected_reason = update_json['rejected_reason']
        if self.rejected_info != update_json['rejected_info']:
            self.rejected_info = update_json['rejected_info']
        if self.lot_id != update_json['lot_id']:
            self.lot_id = update_json['lot_id']
        if self.father_id != update_json['father_id']:
            self.father_id = update_json['father_id']
        if self.mother_id != update_json['mother_id']:
            self.mother_id = update_json['mother_id']


class AnimalChangelog(ChangeLog):
    __tablename__ = 'animal_changelog'


@event.listens_for(Animal.father_id, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.id, initiator.key, str(old_value), str(new_value))


@event.listens_for(Animal.mother_id, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.id, initiator.key, str(old_value), str(new_value))


@event.listens_for(Animal.lot_id, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.id, initiator.key, str(old_value), str(new_value))


@event.listens_for(Animal.rejected_at, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.id, initiator.key, str(old_value), str(new_value))


@event.listens_for(Animal.rejected_reason, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Animal.rejected_info, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


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
