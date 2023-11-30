from app.model.farm import Farm
from app.db.database import db
from sqlalchemy.orm import Query


def updateFarm(request_data):
    if 'id' in request_data:
        farm = Farm.query.filter_by(id=request_data['id']).first()
    else:
        farm = Farm()
    farm.name = request_data['name']
    db.session.add(farm)
    db.session.commit()
    return farm


def get_all_farms():
    return [Farm.serialize(farm) for farm in Farm.query.all()]


def query_farm_by_id(farm_id) -> Query:
    return Farm.query.filter_by(id=farm_id)
