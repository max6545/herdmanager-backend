import logging
from http import HTTPStatus
from flask_restful import Resource, request
from flask import jsonify
from app.model.user import User, Roles
from app.db.database import db
from app.service.authorization.authorization_helper import check_access


class UserList(Resource):
    @check_access([Roles.ADMIN])
    def get(self):
        return jsonify([User.serialize(user) for user in User.query.all()])


class UserGet(Resource):
    @check_access([Roles.ADMIN])
    def get(self, user_id):
        return jsonify(User.query.filter_by(id=user_id).first_or_404().serialize())

    @check_access([Roles.ADMIN])
    def post(self, user_id):
        request_data = request.json
        if user_id != 'undefined':
            user = updateUser(request_data,user_id)
            return {'msg': user.serialize()}, HTTPStatus.OK
        else:
            user = createUser(request_data)
            return {'msg': user.serialize()}, HTTPStatus.CREATED


def updateUser(request_data, user_id):
    user = User.query.filter_by(id=user_id).first()
    user.name = request_data['name']
    user.roles = request_data['roles']
    if 'farm' in request_data:
        user.farm_id = request_data['farm']['id']
    else:
        user.farm_id = None
    db.session.add(user)
    db.session.commit()
    return user


def createUser(request_data):
    user = User.create_user(request_data['name'], request_data['password'])
    user.roles = request_data['roles']
    if 'farm' in request_data:
        user.farm_id = request_data['farm']['id']
    else:
        user.farm_id = None
    db.session.add(user)
    db.session.commit()
    return user
