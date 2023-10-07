from http import HTTPStatus
from datetime import datetime
from flask import request
from flask_restful import Resource
import time
from model.animal import Animal

synchronizedTables = ['animal', 'group', 'animal_parents', 'group_animals']


def getDeletedObjectIds(tablename, timestamp):
    if tablename == 'animal':
        Animal.query.filter_by(deleted=True )
        
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


class SynchronizeDB(Resource):
    @staticmethod
    # @jwt_required()
    def get():
        timestamp = time.mktime(datetime.now().timetuple())
        print(request.args)
        if request.args['lastPulledAt']:
            print(request.args['lastPulledAt'])
        # method returns changes since last sync
        changesObject = {}
        for tablename in synchronizedTables:
            changesObject[tablename] = getChangesObject(tablename, timestamp)
        response = {
            'changes': changesObject,
            'timestamp': timestamp
        }
        print(response)
        return response, HTTPStatus.OK

    @staticmethod
    # @jwt_required()
    def post():
        # methods synchronizes backendDB with clientDB with respect to incoming changes
        request.get_json(force=True)
        print(request.data)
        return None, HTTPStatus.NOT_FOUND
