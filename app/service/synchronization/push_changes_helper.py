from app.model.watermelon_model import WatermelonModel
from app.db.database import db
from flask_jwt_extended import get_jwt_identity
from app.model.user import User


def synchronize(watermelon_class: WatermelonModel, changes_json):
    created = changes_json['created']
    updated = changes_json['updated']
    deleted = changes_json['deleted']
    for object_json in created:
        create_object(watermelon_class, object_json)
    for object_json in updated:
        update_object(watermelon_class, object_json)
    for object_id in deleted:
        delete_object(watermelon_class, object_id)
    db.session.commit()


def create_object(watermelon_class: WatermelonModel, object_json):
    new_object = watermelon_class.create_from_json(object_json=object_json,
                                                   farm_id=User.query.filter_by(id=get_jwt_identity()).first().farm_id)
    db.session.add(new_object)


def update_object(watermelon_class: WatermelonModel, object_json):
    object_to_update = watermelon_class.query.filter_by(watermelon_id=object_json['id']).first()
    if object_to_update is not None:
        object_to_update.update_from_json(object_json)
        db.session.add(object_to_update)
    else:
        create_object(watermelon_class, object_json)


def delete_object(watermelon_class: WatermelonModel, watermelon_id: str):
    class_object = watermelon_class.query.filter_by(watermelon_id=watermelon_id).first()
    if class_object is not None:
        db.session.delete(class_object)
