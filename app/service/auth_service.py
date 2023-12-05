import datetime
import logging
from http import HTTPStatus

from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from flask_restful import Resource

from app.model.user import User, Roles
from app.service.authorization.authorization_helper import check_access
from app.service.parsers import user_parser


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
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        refresh_token = create_refresh_token(identity=str(user.id), expires_delta=expires)
        return (
            {
                'token': access_token,
                'refresh': refresh_token,
                "expires_in": expires.total_seconds(),
                'roles': user.roles
            }, HTTPStatus.OK)


class RefreshToken(Resource):

    @staticmethod
    @check_access([Roles.FARMER])
    def post():
        expires = datetime.timedelta(days=7)
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, expires_delta=expires)
        return {'token': access_token}, HTTPStatus.OK
