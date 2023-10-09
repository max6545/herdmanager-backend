from model.group_animals import GroupAnimals, GroupAnimalsChangelog
from db.database import db
from model.watermelon_model import ChangeOperationType


def synchronize_group_animals(param):
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
    new_relation = GroupAnimals(watermelon_id=relation_json['id'], group_id=relation_json['group_id'],
                                animal_id=relation_json['animal_id'])
    db.session.add(new_relation)


def update_relation(relation_json):
    relation_to_update = GroupAnimals.query.filter_by(watermelon_id=relation_json['id']).first()
    if relation_to_update is not None:
        if relation_to_update.group_id != relation_json['group_id']:
            relation_to_update.group_id = relation_json['group_id']
        if relation_to_update.animal_id != relation_json['animal_id']:
            relation_to_update.animal_id = relation_json['animal_id']
        db.session.add(relation_to_update)


def delete_relation(relation_id):
    relation = GroupAnimals.query.filter_by(watermelon_id=relation_id).first()
    if relation is not None:
        db.session.delete(relation)


def get_group_animals_changes(timestamp_as_datetime):
    return {
        'created': get_created_objects(timestamp_as_datetime),
        'updated': get_updated_objects(timestamp_as_datetime),
        'deleted': get_deleted_object_ids(timestamp_as_datetime)
    }


def get_deleted_object_ids(timestamp_as_datetime):
    delete_changelogs = (GroupAnimalsChangelog.query
                         .filter(GroupAnimalsChangelog.action_at >= timestamp_as_datetime,
                                 GroupAnimalsChangelog.operation == ChangeOperationType.DELETE).all())
    delete_ids = []
    for changelog in delete_changelogs:
        delete_ids.append(changelog.watermelon_id)
    return delete_ids


def get_created_objects(timestamp_as_datetime):
    created_relations = (GroupAnimals.query
                         .filter(GroupAnimals.created_at >= timestamp_as_datetime).all())
    relation_array = []
    for relation in created_relations:
        relation_array.append(relation.watermelon_representation())
    return relation_array


def get_updated_objects(timestamp_as_datetime):
    updated_relations = (GroupAnimals.query
                         .filter(GroupAnimals.last_changed_at >= timestamp_as_datetime,
                                 GroupAnimals.created_at <= timestamp_as_datetime).all())
    relation_array = []
    for relation in updated_relations:
        relation_array.append(relation.watermelon_representation())
    return relation_array
