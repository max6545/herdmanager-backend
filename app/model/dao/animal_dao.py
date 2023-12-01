from app.model.animal import Animal, HerdAnimalType
from app.model.user import User


def get_herd_animals(user_id: int):
    farm_id: int = User.query.filter_by(id=user_id).first().farm_id
    return (Animal.query
            .filter(Animal.farm_id == farm_id)
            .filter(Animal.animal_type in [HerdAnimalType.list()])
            .filter(Animal.rejected_at is None)
            .all())


def get_other_animals(user_id: int):
    farm_id: int = User.query.filter_by(id=user_id).first().farm_id
    return (Animal.query
            .filter(Animal.farm_id == farm_id)
            .filter(Animal.animal_type not in [HerdAnimalType.list()])
            .filter(Animal.rejected_at is None)
            .all())


def get_rejected_animals(user_id: int):
    farm_id: int = User.query.filter_by(id=user_id).first().farm_id
    return (Animal.query
            .filter(Animal.farm_id == farm_id)
            .filter(Animal.rejected_at is not None)
            .all())
