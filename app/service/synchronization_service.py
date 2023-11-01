from http import HTTPStatus
from datetime import datetime
from flask import request, current_app as app
from flask_restful import Resource
from app.model.mobile_device import MobileDevice
from app.db.database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.service.synchronization.service_helper import get_all_changes, get_initial_changes, sync_data
from app.model.model_helper import get_datetime_from_epoch, get_epoch_from_datetime
from flask import current_app as app


class SynchronizeDB(Resource):
    @staticmethod
    @jwt_required()
    def get():
        timestamp = get_epoch_from_datetime(datetime.now())

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
            app.logger.debug(f'Changes after {request.args["lastPulledAt"]}')
            last_pulled_at = get_datetime_from_epoch(int(request.args['lastPulledAt']))
            changes_object = get_all_changes(last_pulled_at, int(request.args['schemaVersion']))
        else:
            app.logger.debug('Returning inital Changes for empty DB')
            changes_object = get_initial_changes()

        response = {
            'changes': changes_object,
            'timestamp': timestamp
        }
        app.logger.debug(response)
        return response, HTTPStatus.OK

    @staticmethod
    @jwt_required()
    def post():
        # methods synchronizes backendDB with clientDB with respect to incoming changes
        app.logger.debug('POST')
        json = request.get_json(force=True)
        app.logger.debug(json)
        if 'data' in json:
            data = json['data']
            last_pulled_at = get_datetime_from_epoch(json['lastPulledAt'])
            sync_data(data, last_pulled_at)

        return [], HTTPStatus.OK
