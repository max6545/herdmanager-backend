from flask import current_app as app
from app.service.synchronization.pull_changes_helper import get_pull_changes
from datetime import datetime
from app.model.animal import Animal, AnimalChangelog
from app.model.group import Group, GroupChangelog
from app.model.animal_parents import AnimalParents, AnimalParentsChangelog
from app.model.group_animals import GroupAnimals, GroupAnimalsChangelog
from app.service.synchronization.push_changes_helper import synchronize
from app.model.model_helper import get_epoch_from_datetime

table_class_mapping = {
    'animal': {
        'model': Animal,
        'changelog': AnimalChangelog
    },
    'group': {
        'model': Group,
        'changelog': GroupChangelog
    },
    'animal_parents': {
        'model': AnimalParents,
        'changelog': AnimalParentsChangelog
    },
    'group_animals': {
        'model': GroupAnimals,
        'changelog': GroupAnimalsChangelog
    },
}


def sync_data(sync_json, last_pulled_at:datetime):
    for table_name in table_class_mapping.keys():
        sync_table(table_name, sync_json[table_name], last_pulled_at)


def sync_table(table_name: str, table_data, last_pulled_at:datetime):
    if table_class_mapping[table_name]:
        synchronize(table_class_mapping[table_name]['model'], table_data,last_pulled_at)
    else:
        app.logger.warning(f'Import for table [{table_name}] not implemented')


def get_changes_object(table_name: str, timestamp_as_datetime, migration_number: int = 11):
    if table_class_mapping[table_name]:
        return get_pull_changes(table_class_mapping[table_name]['model'], table_class_mapping[table_name]['changelog'],
                                timestamp_as_datetime, migration_number)
    else:
        app.logger.warning(f'Changes for [{table_name}] not implemented')
        return {
            'created': [],
            'updated': [],
            'deleted': []
        }


def get_initial_changes():
    changes_object = get_all_changes(datetime.fromtimestamp(0))
    for table_name in table_class_mapping.keys():
        changes_object[table_name]['updated'] = []
        changes_object[table_name]['deleted'] = []
    return changes_object


def get_all_changes(timestamp_as_datetime, migration_number: int = 11):
    changes_object = {}
    for table_name in table_class_mapping.keys():
        changes_object[table_name] = get_changes_object(table_name, timestamp_as_datetime, migration_number)
    return changes_object
