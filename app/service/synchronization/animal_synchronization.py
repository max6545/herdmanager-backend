from model.animal import Animal
from db.database import db
from datetime import datetime


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
                        earTag=animal_json['ear_tag'], born_at=datetime.fromtimestamp(animal_json['born_at'] / 1000),
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
        if animal_to_update.born_at != datetime.fromtimestamp(animal_json['born_at'] / 1000):
            animal_to_update.born_at = datetime.fromtimestamp(animal_json['born_at'] / 1000)
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
