from db.database import db
from model.animal_parents import AnimalParents, AnimalParentsChangelog
from datetime import datetime
from model.watermelon_model import ChangeOperationType


def synchronize_animal_parents(param):
    created = param['created']
    updated = param['updated']
    deleted = param['deleted']
    for relation in created:
        create_relation(relation)
    for relation in updated:
        update_relation(relation)
    for relation_id in deleted:
        delete_relation(relation_id)
    db.session.commit()


def create_relation(relation_json):
    new_relation = AnimalParents(watermelon_id=relation_json['id'], parent_id=relation_json['parent_id'],
                                 child_id=relation_json['child_id'])
    db.session.add(new_relation)


def update_relation(relation_json):
    relation_to_update = AnimalParents.query.filter_by(watermelon_id=relation_json['id']).first()
    if relation_to_update is not None:
        if relation_to_update.parent_id != relation_json['parent_id']:
            relation_to_update.parent_id = relation_json['parent_id']
        if relation_to_update.child_id != relation_json['child_id']:
            relation_to_update.child_id = relation_json['child_id']
        db.session.add(relation_to_update)


def delete_relation(relation_id):
    relation = AnimalParents.query.filter_by(watermelon_id=relation_id).first()
    if relation is not None:
        db.session.delete(relation)


def get_animal_parents_changes(timestamp):
    return {
        'created': get_created_objects(timestamp),
        'updated': get_updated_objects(timestamp),
        'deleted': get_deleted_object_ids(timestamp)
    }


def get_deleted_object_ids(timestamp_as_datetime: datetime):
    delete_changelogs = (AnimalParentsChangelog.query
                         .filter(AnimalParentsChangelog.action_at >= timestamp_as_datetime,
                                 AnimalParentsChangelog.operation == ChangeOperationType.DELETE).all())
    delete_ids = []
    for changelog in delete_changelogs:
        delete_ids.append(changelog.watermelon_id)
    return delete_ids


def get_created_objects(timestamp_as_datetime):
    created_relations = AnimalParents.query.filter(AnimalParents.created_at >= timestamp_as_datetime).all()
    relation_array = []
    for relation in created_relations:
        relation_array.append(relation.watermelon_representation())
    return relation_array


def get_updated_objects(timestamp_as_datetime):
    updated_relations = AnimalParents.query.filter(AnimalParents.last_changed_at >= timestamp_as_datetime,
                                                   AnimalParents.created_at <= timestamp_as_datetime).all()
    relation_array = []
    for relation in updated_relations:
        relation_array.append(relation.watermelon_representation())
    return relation_array
