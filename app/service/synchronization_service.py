from http import HTTPStatus
from datetime import datetime
from flask import request
from flask_restful import Resource
import time
from service.synchronization.animal_synchronization import synchronize_animals, get_animal_changes
from service.synchronization.group_synchronization import synchronize_groups, get_group_changes
from service.synchronization.group_animals_synchronization import synchronize_group_animals, get_group_animals_changes
from service.synchronization.animal_parents_synchronization import synchronize_animal_parents, \
    get_animal_parents_changes

synchronizedTables = ['animal', 'group', 'animal_parents', 'group_animals']


def get_all_changes(timestamp_as_datetime):
    changes_object = {}
    for table_name in synchronizedTables:
        changes_object[table_name] = get_changes_object(table_name, timestamp_as_datetime)
    return changes_object


def get_changes_object(table_name: str, timestamp_as_datetime):
    match table_name:
        case 'animal':
            return get_animal_changes(timestamp_as_datetime)
        case 'group':
            return get_group_changes(timestamp_as_datetime)
        case 'group_animals':
            return get_group_animals_changes(timestamp_as_datetime)
        case 'animal_parents':
            return get_animal_parents_changes(timestamp_as_datetime)
        case _:
            print(f'Changes for [{table_name}] not implemented')
            return {
                'created': [],
                'updated': [],
                'deleted': []
            }


def sync_table(table_name: str, table_data):
    match table_name:
        case 'animal':
            synchronize_animals(table_data)
        case 'group':
            synchronize_groups(table_data)
        case 'group_animals':
            synchronize_group_animals(table_data)
        case 'animal_parents':
            synchronize_animal_parents(table_data)
        case _:
            print(f'Import for table [{table_name}] not implemented')


class SynchronizeDB(Resource):
    @staticmethod
    # @jwt_required()
    def get():
        timestamp = time.mktime(datetime.now().timetuple())
        print(request.args)
        last_pulled_at = datetime.fromtimestamp(0)
        if request.args['lastPulledAt']:
            print(request.args['lastPulledAt'])
            last_pulled_at = datetime.fromtimestamp(int(request.args['lastPulledAt']))
        print(last_pulled_at)
        changes_object = get_all_changes(last_pulled_at)

        response = {
            'changes': changes_object,
            'timestamp': timestamp
        }
        print(response)
        return response, HTTPStatus.OK

    @staticmethod
    # @jwt_required()
    def post():
        # methods synchronizes backendDB with clientDB with respect to incoming changes
        json = request.get_json(force=True)
        if 'data' in json:
            data = json['data']
            for table_name in synchronizedTables:
                if table_name in synchronizedTables:
                    sync_table(table_name, data[table_name])

        return None, HTTPStatus.OK
