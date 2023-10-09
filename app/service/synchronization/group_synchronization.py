from model.group import Group, GroupChangelog
from db.database import db
from model.watermelon_model import ChangeOperationType


def synchronize_groups(param):
    created = param['created']
    updated = param['updated']
    deleted = param['deleted']
    for group in created:
        create_group(group)
    for group in updated:
        update_group(group)
    for group_id in deleted:
        delete_group(group_id)
    db.session.commit()


def create_group(group_json):
    new_group = Group(watermelon_id=group_json['id'], name=group_json['name'])
    db.session.add(new_group)


def update_group(group_json):
    group_to_update = Group.query.filter_by(watermelon_id=group_json['id']).first()
    if group_to_update is not None:
        if group_to_update.name != group_json['name']:
            group_to_update.name = group_json['name']
        db.session.add(group_to_update)


def delete_group(group_id):
    group = Group.query.filter_by(watermelon_id=group_id).first()
    if group is not None:
        db.session.delete(group)


def get_group_changes(timestamp_as_datetime):
    return {
        'created': get_created_objects(timestamp_as_datetime),
        'updated': get_updated_objects(timestamp_as_datetime),
        'deleted': get_deleted_object_ids(timestamp_as_datetime)
    }


def get_deleted_object_ids(timestamp_as_datetime):
    delete_changelogs = GroupChangelog.query.filter(GroupChangelog.action_at >= timestamp_as_datetime,
                                                    GroupChangelog.operation == ChangeOperationType.DELETE).all()
    delete_ids = []
    for changelog in delete_changelogs:
        delete_ids.append(changelog.watermelon_id)
    return delete_ids


def get_created_objects(timestamp_as_datetime):
    created_relations = Group.query.filter(Group.created_at >= timestamp_as_datetime).all()
    relation_array = []
    for relation in created_relations:
        relation_array.append(relation.watermelon_representation())
    return relation_array


def get_updated_objects(timestamp_as_datetime):
    updated_relations = Group.query.filter(Group.last_changed_at >= timestamp_as_datetime,
                                           Group.created_at <= timestamp_as_datetime).all()
    relation_array = []
    for relation in updated_relations:
        relation_array.append(relation.watermelon_representation())
    return relation_array
