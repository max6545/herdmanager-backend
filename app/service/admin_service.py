import logging
from app.model.user import User, Roles
from app.model.farm import Farm
from flask_restful import Resource
from flask import jsonify
from app.db.database import db
from app.config.database import create_initial_user
import os
from http import HTTPStatus
from app.db.backup_management import get_latest_nc_backup, create_backup
from app.service.authorization.authorization_helper import check_access


class CreateAdminUser(Resource):
    @staticmethod
    @check_access([Roles.ADMIN])
    def get():
        return jsonify({'msg': create_initial_user()}), HTTPStatus.OK


class RestoreDB(Resource):
    @staticmethod
    def get():
        get_latest_nc_backup()


class BackupDB(Resource):
    @staticmethod
    def get():
        backup_name = ''
        try:
            create_backup()
            return {'message': f'Backup has been created on nextcloud [{backup_name}]'}, HTTPStatus.CREATED
        except Exception as e:
            return {'error': e}, HTTPStatus.INTERNAL_SERVER_ERROR
