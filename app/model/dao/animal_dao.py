import datetime

from app.model.animal import Animal, HerdAnimalType
from app.model.user import User
from app.model.model_helper import get_datetime_from_epoch


def get_herd_animals(user_id: int):
    farm_id: int = User.query.filter_by(id=user_id).first().farm_id
    return (Animal.query
            .filter(Animal.farm_id == farm_id)
            .filter(Animal.animal_type.in_(HerdAnimalType.list()))
            .filter(Animal.rejected_at == get_datetime_from_epoch(0))
            .all())


def get_other_animals(user_id: int):
    farm_id: int = User.query.filter_by(id=user_id).first().farm_id
    return (Animal.query
            .filter(Animal.farm_id == farm_id)
            .filter(Animal.animal_type.notin_(HerdAnimalType.list()))
            .filter(Animal.rejected_at == get_datetime_from_epoch(0))
            .all())


def get_rejected_animals(user_id: int):
    farm_id: int = User.query.filter_by(id=user_id).first().farm_id
    return (Animal.query
            .filter(Animal.farm_id == farm_id)
            .filter(Animal.rejected_at > get_datetime_from_epoch(0))
            .all())
