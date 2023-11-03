from app.model.watermelon_model import WatermelonModel, ChangeLog, ChangeOperationType
from app.model.user import User
from flask_jwt_extended import get_jwt_identity
from datetime import datetime


def get_pull_changes(watermelon_class: WatermelonModel, changelog_class: ChangeLog,
                     timestamp_as_datetime: datetime, migration_number: int = 11):
    return {
        'created': get_created_objects(watermelon_class, timestamp_as_datetime, migration_number),
        'updated': get_updated_objects(watermelon_class, timestamp_as_datetime, migration_number),
        'deleted': get_deleted_object_ids(changelog_class, timestamp_as_datetime)
    }


def get_created_objects(class_name: WatermelonModel, timestamp_as_datetime: datetime, migration_number: int = 11):
    farm_id = User.query.filter_by(id=get_jwt_identity()).first().farm_id
    created_relations = (class_name.query
                         .filter(class_name.created_at > timestamp_as_datetime)
                         .filter(class_name.farm_id == farm_id)
                         .all())
    relation_array = []
    for relation in created_relations:
        relation_array.append(relation.watermelon_representation(migration_number=migration_number))
    return relation_array


def get_updated_objects(class_name: WatermelonModel, timestamp_as_datetime: datetime, migration_number: int = 11):
    farm_id = User.query.filter_by(id=get_jwt_identity()).first().farm_id
    updated_relations = (class_name.query
                         .filter(class_name.last_changed_at >= timestamp_as_datetime)
                         .filter(class_name.created_at <= timestamp_as_datetime)
                         .filter(class_name.farm_id == farm_id)
                         .all())
    relation_array = []
    for relation in updated_relations:
        relation_array.append(relation.watermelon_representation(migration_number=migration_number))
    return relation_array


def get_deleted_object_ids(class_name: ChangeLog, timestamp_as_datetime: datetime):
    farm_id = User.query.filter_by(id=get_jwt_identity()).first().farm_id
    deleted_relations = class_name.query.filter(
        class_name.action_at >= timestamp_as_datetime,
        class_name.operation == ChangeOperationType.DELETE,
        class_name.farm_id == farm_id).all()
    relation_array = []
    for relation in deleted_relations:
        relation_array.append(relation.watermelon_id)
    return relation_array
