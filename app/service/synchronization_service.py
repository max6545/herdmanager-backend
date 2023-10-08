from http import HTTPStatus
from datetime import datetime
from flask import request
from flask_restful import Resource
import time
from model.animal import AnimalChangelog
from model.watermelon_model import ChangeOperationType
from service.synchronization.animal_synchronization import synchronize_animals
from service.synchronization.group_synchronization import synchronize_groups

synchronizedTables = ['animal', 'group', 'animal_parents', 'group_animals']


def getDeletedObjectIds(tablename, timestamp):
    if tablename == 'animal':
        return (AnimalChangelog.query
                .filter(
            AnimalChangelog.action_at >= datetime.fromtimestamp(timestamp),
            AnimalChangelog.operation == ChangeOperationType.DELETE)
                .with_entities(
            AnimalChangelog.watermelon_id)
                .all())
    return []


def getCreatedObjects(tablename, timestamp):
    return []


def getUpdatedObjects(tablename, timestamp):
    return []


def getChangesObject(tablename, timestamp):
    return {
        'created': getCreatedObjects(tablename, timestamp),
        'updated': getUpdatedObjects(tablename, timestamp),
        'deleted': getDeletedObjectIds(tablename, timestamp)
    }


def sync_table(table_name: str, param):
    match table_name:
        case 'animal':
            synchronize_animals(param)
        case 'group':
            synchronize_groups(param)
        case _:
            print(f'Import for table [{table_name}] not implemented')


class SynchronizeDB(Resource):
    @staticmethod
    # @jwt_required()
    def get():
        timestamp = time.mktime(datetime.now().timetuple())
        print(request.args)
        if request.args['lastPulledAt']:
            print(request.args['lastPulledAt'])
        # method returns changes since last sync
        changes_object = {}
        for table_name in synchronizedTables:
            changes_object[table_name] = getChangesObject(table_name, timestamp)
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
