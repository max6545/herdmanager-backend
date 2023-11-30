import logging
from http import HTTPStatus
from flask_restful import Resource, request
from flask import jsonify
from app.model.user import User
from flask_jwt_extended import jwt_required
from app.db.database import db


class UserList(Resource):
    @staticmethod
    @jwt_required()
    def get():
        return jsonify([User.serialize(user) for user in User.query.all()])


class UserGet(Resource):
    @staticmethod
    @jwt_required()
    def get():
        return jsonify(User.query.filter_by(id=request.args['id']).first_or_404().serialize())

    @staticmethod
    @jwt_required()
    def post():
        request_data = request.json
        if 'id' in request_data:
            user = updateUser(request_data)
            return {'msg': user.serialize()}, HTTPStatus.OK
        else:
            user = createUser(request_data)
            return {'msg': user.serialize()}, HTTPStatus.CREATED


def updateUser(request_data):
    user = User.query.filter_by(id=request_data['id']).first()
    user.name = request_data['name']
    if 'farm' in request_data:
        user.farm_id = request_data['farm']['id']
    else:
        user.farm_id = None
    db.session.add(user)
    db.session.commit()
    return user


def createUser(request_data):
    user = User.create_user(request_data['name'], request_data['password'])

    if 'farm' in request_data:
        user.farm_id = request_data['farm']['id']
    else:
        user.farm_id = None
    db.session.add(user)
    db.session.commit()
    return user
