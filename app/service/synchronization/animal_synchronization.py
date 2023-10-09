import json

from model.animal import Animal, AnimalChangelog
from db.database import db
from datetime import datetime
from model.watermelon_model import ChangeOperationType


def synchronize_animals(param):
    created = param['created']
    updated = param['updated']
    deleted = param['deleted']
    for animal in created:
        create_animal(animal)
    for animal in updated:
        update_animal(animal)
    for animal_id in deleted:
        delete_animal(animal_id)
    db.session.commit()


def create_animal(animal_json):
    new_animal = Animal(watermelon_id=animal_json['id'], sex=animal_json['sex'], animal_type=animal_json['animal_type'],
                        earTag=animal_json['ear_tag'], born_at=datetime.fromtimestamp(animal_json['born_at']),
                        farmCode=animal_json['farm_code'], countryCode=animal_json['country_code'],
                        name=animal_json['name'])
    db.session.add(new_animal)


def update_animal(animal_json):
    animal_to_update = Animal.query.filter_by(watermelon_id=animal_json['id']).first()
    if animal_to_update is not None:
        if animal_to_update.sex != animal_json['sex']:
            animal_to_update.sex = animal_json['sex']
        if animal_to_update.animal_type != animal_json['animal_type']:
            animal_to_update.animal_type = animal_json['animal_type']
        if animal_to_update.earTag != animal_json['ear_tag']:
            animal_to_update.earTag = animal_json['ear_tag']
        if animal_to_update.born_at != datetime.fromtimestamp(animal_json['born_at']):
            animal_to_update.born_at = datetime.fromtimestamp(animal_json['born_at'])
        if animal_to_update.countryCode != animal_json['country_code']:
            animal_to_update.countryCode = animal_json['country_code']
        if animal_to_update.farmCode != animal_json['farm_code']:
            animal_to_update.farmCode = animal_json['farm_code']
        if animal_to_update.name != animal_json['name']:
            animal_to_update.name = animal_json['name']
        db.session.add(animal_to_update)


def delete_animal(animal_id):
    animal = Animal.query.filter_by(watermelon_id=animal_id).first()
    if animal is not None:
        db.session.delete(animal)


def get_animal_changes(timestamp_as_datetime):
    return {
        'created': get_created_objects(timestamp_as_datetime),
        'updated': get_updated_objects(timestamp_as_datetime),
        'deleted': get_deleted_object_ids(timestamp_as_datetime)
    }


def get_deleted_object_ids(timestamp_as_datetime: datetime):
    deleted_relations = AnimalChangelog.query.filter(
        AnimalChangelog.action_at >= timestamp_as_datetime,
        AnimalChangelog.operation == ChangeOperationType.DELETE).all()
    relation_array = []
    for relation in deleted_relations:
        relation_array.append(relation.watermelon_id)
    return relation_array


def get_created_objects(timestamp_as_datetime):
    created_relations = Animal.query.filter(Animal.created_at >= timestamp_as_datetime).all()
    relation_array = []
    for relation in created_relations:
        relation_array.append(relation.watermelon_representation())
    return relation_array


def get_updated_objects(timestamp_as_datetime):
    updated_relations = Animal.query.filter(Animal.last_changed_at >= timestamp_as_datetime,
                                            Animal.created_at <= timestamp_as_datetime).all()
    relation_array = []
    for relation in updated_relations:
        relation_array.append(relation.watermelon_representation())
    return relation_array
