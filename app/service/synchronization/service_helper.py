from datetime import datetime

from flask import current_app as app

from app import MobileDevice
from app.db.database import db
from app.model.animal import Animal, AnimalChangelog
from app.model.animal_tags import AnimalTags, AnimalTagsChangelog
from app.model.configuration import Configuration, ConfigurationChangelog
from app.model.event import Event, EventChangelog
from app.model.group import Group, GroupChangelog
from app.model.groupHistory import GroupHistory, GroupHistoryChangelog, GroupHistoryOldMembers, GroupHistoryNewMembers, \
    GroupHistoryOldMembersChangelog, GroupHistoryNewMembersChangelog
from app.model.group_animals import GroupAnimals, GroupAnimalsChangelog
from app.model.lot import Lot, LotChangelog
from app.model.lotHistory import LotHistory, LotHistoryChangelog, LotHistoryOldMembers, LotHistoryNewMembers, \
    LotHistoryOldMembersChangelog, LotHistoryNewMembersChangelog
from app.model.model_helper import get_datetime_from_epoch
from app.model.tag import Tag, TagChangelog
from app.model.treatment import Treatment, TreatmentChangelog
from app.model.treatment_animals import TreatmentAnimals, TreatmentAnimalsChangelog
from app.service.synchronization.pull_changes_helper import get_pull_changes
from app.service.synchronization.push_changes_helper import synchronize

table_class_mapping = {
    'animal': {
        'model': Animal,
        'changelog': AnimalChangelog
    },
    'group': {
        'model': Group,
        'changelog': GroupChangelog
    },
    'group_animals': {
        'model': GroupAnimals,
        'changelog': GroupAnimalsChangelog
    },
    'group_history': {
        'model': GroupHistory,
        'changelog': GroupHistoryChangelog
    },
    'group_history_old_members': {
        'model': GroupHistoryOldMembers,
        'changelog': GroupHistoryOldMembersChangelog
    },
    'group_history_new_members': {
        'model': GroupHistoryNewMembers,
        'changelog': GroupHistoryNewMembersChangelog
    },
    'tag': {
        'model': Tag,
        'changelog': TagChangelog
    },
    'animal_tags': {
        'model': AnimalTags,
        'changelog': AnimalTagsChangelog
    },
    'configuration': {
        'model': Configuration,
        'changelog': ConfigurationChangelog
    },
    'event': {
        'model': Event,
        'changelog': EventChangelog
    },
    'lot': {
        'model': Lot,
        'changelog': LotChangelog
    },
    'lot_history': {
        'model': LotHistory,
        'changelog': LotHistoryChangelog
    },
    'lot_history_old_members': {
        'model': LotHistoryOldMembers,
        'changelog': LotHistoryOldMembersChangelog
    },
    'lot_history_new_members': {
        'model': LotHistoryNewMembers,
        'changelog': LotHistoryNewMembersChangelog
    },
    'treatment': {
        'model': Treatment,
        'changelog': TreatmentChangelog
    },
    'treatment_animals': {
        'model': TreatmentAnimals,
        'changelog': TreatmentAnimalsChangelog
    },
}


def push_data(json_data, push_timestamp: datetime, schema_version: int, user_id: int):
    for table_name in table_class_mapping.keys():
        if table_name in json_data:
            sync_table(table_name, json_data[table_name], push_timestamp, schema_version, user_id)
        else:
            app.logger.warning(f'Tablename [{table_name}] missing in json')


def sync_table(table_name: str, table_data, last_pulled_at: datetime, schema_version: int, user_id: int):
    if table_class_mapping[table_name]:
        synchronize(table_class_mapping[table_name]['model'], table_data, last_pulled_at, schema_version, user_id)
    else:
        app.logger.warning(f'Import for table [{table_name}] not implemented')


def get_changes_object(table_name: str, timestamp_as_datetime, user_id: int, migration_number: int):
    if table_class_mapping[table_name]:
        return get_pull_changes(table_class_mapping[table_name]['model'], table_class_mapping[table_name]['changelog'],
                                timestamp_as_datetime, user_id, migration_number)
    else:
        app.logger.warning(f'Changes for [{table_name}] not implemented')
        return {
            'created': [],
            'updated': [],
            'deleted': []
        }


def create_pull_response(last_pulled_at, migration_number: int, request_start_time_epoch: int, user_id: int):
    response = {
        'changes': get_changes(last_pulled_at, user_id, migration_number),
        'timestamp': request_start_time_epoch
    }
    app.logger.debug('PULL RESPONSE CREATED')
    # app.logger.debug(response)
    return response


def get_changes(timestamp, user_id: int, migration_number: int):
    if timestamp is not None:
        app.logger.debug(f'Changes after {timestamp}')
        return get_all_changes(timestamp, user_id, migration_number)
    else:
        app.logger.debug('Returning inital Changes for empty DB')
        return get_initial_changes(user_id, migration_number)


def get_initial_changes(user_id: int, migration_number: int):
    changes_object = get_all_changes(datetime.fromtimestamp(0), user_id, migration_number)
    for table_name in table_class_mapping.keys():
        changes_object[table_name]['updated'] = []
        changes_object[table_name]['deleted'] = []
    return changes_object


def get_all_changes(timestamp_as_datetime, user_id: int, migration_number: int):
    changes_object = {}
    for table_name in table_class_mapping.keys():
        changes_object[table_name] = get_changes_object(table_name, timestamp_as_datetime, user_id, migration_number)
    return changes_object


def update_mobile_device(unique_id: str, now_epoch: int, user_id):
    md = MobileDevice.query.filter(MobileDevice.name == unique_id).first()
    if md is not None:
        md.last_pull_at = get_datetime_from_epoch(now_epoch)
    else:
        md = MobileDevice(name=unique_id, user_id=user_id)
    db.session.add(md)
    db.session.commit()
