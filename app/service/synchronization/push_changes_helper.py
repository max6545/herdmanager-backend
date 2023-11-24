from app.model.watermelon_model import WatermelonModel
from app.db.database import db
from app.model.user import User
from datetime import datetime


def synchronize(watermelon_class: WatermelonModel, changes_json, last_pulled_at: datetime, schema_version: int,
                user_id: int):
    created = changes_json['created']
    updated = changes_json['updated']
    deleted = changes_json['deleted']
    for object_json in created:
        create_object(watermelon_class, object_json, last_pulled_at, user_id)
    for object_json in updated:
        update_object(watermelon_class, object_json, last_pulled_at, schema_version, user_id)
    for object_id in deleted:
        delete_object(watermelon_class, object_id)
    db.session.commit()


def create_object(watermelon_class: WatermelonModel, object_json, last_pulled_at: datetime, user_id):
    new_object = watermelon_class(object_json=object_json,
                                  farm_id=User.query.filter_by(id=user_id).first().farm_id,
                                  last_pulled_at=last_pulled_at)
    db.session.add(new_object)


def update_object(watermelon_class: WatermelonModel, object_json, last_pulled_at: datetime, schema_version: int,
                  user_id):
    object_to_update = watermelon_class.query.filter_by(watermelon_id=object_json['id']).first()
    if object_to_update is not None:
        object_to_update.update_from_json(object_json, last_pulled_at=last_pulled_at, migration_number=schema_version)
        db.session.add(object_to_update)
    else:
        create_object(watermelon_class, object_json, last_pulled_at, user_id)


def delete_object(watermelon_class: WatermelonModel, watermelon_id: str):
    class_object = watermelon_class.query.filter_by(watermelon_id=watermelon_id).first()
    if class_object is not None:
        db.session.delete(class_object)
