from enum import Enum, auto

from sqlalchemy import event
from db.database import db
from model.watermelon_model import WatermelonModel, ChangeLog


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
    farmCode = db.Column(db.String(255))
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'))

    def serialize(self):
        return {
            'id': self.id,
            'watermelon_id': self.watermelon_id,
            'earTag': self.earTag,
            'name': self.name
        }


@event.listens_for(Animal, 'after_insert')
def receive_after_insert(mapper, connection, target):
    print('CreatedAnimal')
    print(target.serialize())


@event.listens_for(Animal.name, 'set')
def receive_set(target, value, oldvalue, initiator):
    print(f"name set: {value} and id is {target.id}")
    

@event.listens_for(Animal, 'before_update')
def receive_before_update(mapper, connection, target):
    print('Animal will be update: ' + target.serialize())


class AnimalChangelog(ChangeLog):
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'))