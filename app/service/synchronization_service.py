from http import HTTPStatus
from datetime import datetime
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.service.synchronization.service_helper import push_data, update_mobile_device, create_pull_response
from app.model.model_helper import get_datetime_from_epoch
from flask import current_app as app


class SynchronizeDB(Resource):
    @staticmethod
    @jwt_required()
    def get():
        request_start_time = datetime.now()
        last_pulled_at = None
        migration_number = None

        if request.args['uniqueId']:
            update_mobile_device(request.args['uniqueId'], request_start_time, get_jwt_identity())
        if request.args['lastPulledAt'] and request.args['lastPulledAt'] != 'null':
            last_pulled_at = get_datetime_from_epoch(int(request.args['lastPulledAt']))
        if request.args['schemaVersion']:
            migration_number = get_datetime_from_epoch(int(request.args['schemaVersion']))

        pull_response = create_pull_response(last_pulled_at, migration_number, request_start_time, get_jwt_identity())
        return pull_response, HTTPStatus.OK

    @staticmethod
    @jwt_required()
    def post():
        # methods synchronizes backendDB with clientDB with respect to incoming changes
        app.logger.debug('POST')
        json = request.get_json(force=True)
        app.logger.debug(json)
        if 'data' in json:
            push_data(json_data=json['data'],
                      push_timestamp=get_datetime_from_epoch(json['lastPulledAt']),
                      schema_version=int(json['schemaVersion']),
                      user_id=get_jwt_identity()
                      )

        return [], HTTPStatus.OK
