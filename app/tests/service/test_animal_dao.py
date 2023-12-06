import datetime
import logging

from app.model.dao.animal_dao import get_herd_animals, get_other_animals
from app.model.animal import Animal
from app.model.user import User
from app.db.database import db


def test_get_herd_animals(app):
    animal_json = {
        'id': 'WATERMELON_ID', '_status': 'created', '_changed': 'ear_tag', 'animal_type': 'SHEEP',
        'ear_tag': '222222', 'sex': 'F', 'name': None, 'country_code': 'COUNTRY_CODE',
        'born_at': 1700504203888, 'farm_code': 'FARM_CODE', 'description': '', 'rejected_at': 0,
        'rejected_reason': '', 'rejected_info': '', 'lot_id': None, 'father_id': None, 'mother_id': None
    }

    animals = get_herd_animals(1)
    assert len(animals) == 0

    animal = Animal(object_json=animal_json, farm_id=1, last_pulled_at=datetime.datetime.now())
    db.session.add(animal)
    db.session.commit()
    animals = get_herd_animals(1)
    assert len(animals) == 1
    animals = get_other_animals(1)
    assert len(animals) == 0
    animal2 = Animal(object_json=animal_json, farm_id=1, last_pulled_at=datetime.datetime.now())
    animal2.animal_type = 'DOG'
    db.session.add(animal2)
    db.session.commit()
    animals = get_other_animals(1)
    assert len(animals) == 1
