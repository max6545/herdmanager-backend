import datetime
import logging
from http import HTTPStatus

from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from flask_restful import Resource

from app.model.user import User, Roles
from app.service.authorization.authorization_helper import check_access
from app.service.parsers import user_parser
from app.model.model_helper import get_epoch_from_datetime


class LoginApi(Resource):

    @staticmethod
    def post():
        request.get_json()
        args = user_parser.parse_args()
        logging.info(args)
        user = User.query.filter_by(name=args['name']).first_or_404(
            description='User with name={} is not available'.format(args['name']))
        authorized = user.check_password(args['password'])
        if not authorized:
            return {'error': 'Email or password invalid'}, HTTPStatus.UNAUTHORIZED

        expires = datetime.timedelta(days=7)
        refresh_expires = datetime.timedelta(days=10)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        refresh_token = create_refresh_token(identity=str(user.id), expires_delta=refresh_expires)
        return (
            {
                'token': access_token,
                'refresh': refresh_token,
                'roles': user.roles
            }, HTTPStatus.OK)


class RefreshToken(Resource):

    @staticmethod
    @jwt_required(refresh=True)
    def post():
        expires = datetime.timedelta(days=7)
        refresh_expires = datetime.timedelta(days=10)
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, expires_delta=expires)
        refresh_token = create_refresh_token(identity=identity, expires_delta=refresh_expires)
        return {'token': access_token, 'refresh': refresh_token}, HTTPStatus.CREATED
