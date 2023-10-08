from model.group import Group
from db.database import db


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
