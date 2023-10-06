import datetime
import logging
from http import HTTPStatus

from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource

from db.database import db
from model.user import User
from service.parsers import user_parser


class SignupApi(Resource):

    @staticmethod
    @jwt_required()
    def post():
        print('abc')
        request.get_json()
        args = user_parser.parse_args()
        user = User.query.filter_by(name=args['name']).first()
        if user is not None:
            return {'error': 'User with name={} already exists'.format(args['name'])}, HTTPStatus.BAD_REQUEST
        user = User.create_user(args['name'], args['password'])
        db.session.add(user)
        db.session.commit()
        return User.serialize(user), HTTPStatus.CREATED


class LoginApi(Resource):

    @staticmethod
    def post():

        print('vvv')
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
        return {'token': access_token}, HTTPStatus.OK
