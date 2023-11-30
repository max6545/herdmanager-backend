import logging
from http import HTTPStatus
from flask_restful import Resource, request
from flask import jsonify
from app.model.farm import Farm
from flask_jwt_extended import jwt_required
from app.model.dao.farm_dao import updateFarm, get_all_farms, query_farm_by_id


class FarmList(Resource):
    @staticmethod
    @jwt_required()
    def get():
        return jsonify(get_all_farms())


class FarmGet(Resource):
    @staticmethod
    @jwt_required()
    def get():
        return jsonify(query_farm_by_id(request.args['id']).first_or_404().serialize())

    @staticmethod
    @jwt_required()
    def post():
        request_data = request.json
        farm = updateFarm(request_data)
        return {'msg': farm.serialize()}, HTTPStatus.OK if 'id' else HTTPStatus.CREATED
