import logging
from app.model.user import User, Roles
from app.model.farm import Farm
from flask_restful import Resource
from flask import jsonify
from app.db.database import db
import os
from http import HTTPStatus
from app.db.backup_management import get_latest_nc_backup, create_backup
from app.service.authorization.authorization_helper import check_access


class CreateAdminUser(Resource):
    @staticmethod
    @check_access([Roles.ADMIN])
    def get():
        if 'DEFAULT_USERNAME' in os.environ and 'DEFAULT_PASSWORD' in os.environ:
            username = os.getenv('DEFAULT_USERNAME')
            password = os.getenv('DEFAULT_PASSWORD')
        else:
            logging.warning('Variable for DEFAULT_USERNAME and DEFAULT_PASSWORD not set using credentials admin:admin')
            username = 'admin'
            password = 'admin'
        user = User.query.filter_by(name=username).one_or_none()
        if user is None:
            # create new admin if default username/pw is changed and delete all users in db
            default_admin_users = User.query.filter_by(name='admin').first()
            if default_admin_users is not None:
                db.session.delete(default_admin_users)
            user = User.create_user(username, password)
            user.roles = ['admin', 'farmer']
            farm = Farm()
            farm.name = 'TestFarm'
            db.session.add(farm)
            db.session.commit()
            user.farm_id = farm.id
            db.session.add(user)
            db.session.commit()
            logging.info(f'create default user [{username}]')
            return jsonify({'msg': f'create default user[{username}]'}), HTTPStatus.CREATED
        else:
            logging.info(f'defaultuser already exists [{username}]')
            return jsonify({'msg': f'defaultuser already exists [{username}]'}), HTTPStatus.OK


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

