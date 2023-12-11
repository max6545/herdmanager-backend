import time
from http import HTTPStatus

from flask import current_app as app
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource

from app.model.model_helper import get_datetime_from_epoch
from app.model.user import Roles
from app.service.authorization.authorization_helper import check_access
from app.service.synchronization.service_helper import push_data, update_mobile_device, create_pull_response


class SynchronizeDB(Resource):
    @staticmethod
    @check_access([Roles.FARMER])
    def get():
        request_start_time = int(time.time() * 1000)
        last_pulled_at = None
        migration_number = None

        if request.args['uniqueId']:
            update_mobile_device(request.args['uniqueId'], request_start_time, get_jwt_identity())
        if request.args['lastPulledAt'] and request.args['lastPulledAt'] != 'null':
            last_pulled_at = get_datetime_from_epoch(int(request.args['lastPulledAt']))
        if request.args['schemaVersion']:
            migration_number = int(request.args['schemaVersion'])

        pull_response = create_pull_response(last_pulled_at, migration_number, request_start_time, get_jwt_identity())
        return pull_response, HTTPStatus.OK

    @staticmethod
    @check_access([Roles.FARMER])
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
