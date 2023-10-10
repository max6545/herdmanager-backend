from http import HTTPStatus
from datetime import datetime
from flask import request
from flask_restful import Resource
import time
from app.model.mobile_device import MobileDevice
from app.db.database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.service.synchronization.service_helper import get_all_changes, get_initial_changes, sync_data


class SynchronizeDB(Resource):
    @staticmethod
    @jwt_required()
    def get():
        timestamp = time.mktime(datetime.now().timetuple())
        print(request.args)
        print(get_jwt_identity())
        if request.args['uniqueId']:
            md = MobileDevice.query.filter(MobileDevice.name == request.args['uniqueId']).first()
            if md is not None:
                md.last_pull_at = datetime.now()
            else:
                md = MobileDevice(name=request.args['uniqueId'], user_id=get_jwt_identity())
            db.session.add(md)
            db.session.commit()

        if (request.args['lastPulledAt'] and request.args['lastPulledAt'] != 'null'
                and request.args['lastPulledAt'] != '0' and request.args['schemaVersion']):
            print(f'SchemaVersion={request.args["schemaVersion"]}')
            last_pulled_at = datetime.fromtimestamp(int(request.args['lastPulledAt']))
            changes_object = get_all_changes(last_pulled_at, request.args['schemaVersion'])
        else:
            changes_object = get_initial_changes()

        response = {
            'changes': changes_object,
            'timestamp': timestamp
        }
        print(response)
        return response, HTTPStatus.OK

    @staticmethod
    @jwt_required()
    def post():
        # methods synchronizes backendDB with clientDB with respect to incoming changes
        print('POST')
        json = request.get_json(force=True)
        print(json)
        if 'data' in json:
            data = json['data']
            sync_data(data)

        return [], HTTPStatus.OK
