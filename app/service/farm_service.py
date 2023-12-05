from http import HTTPStatus

from flask import jsonify
from flask_restful import Resource, request

from app.model.dao.farm_dao import updateFarm, get_all_farms, query_farm_by_id
from app.model.user import Roles
from app.service.authorization.authorization_helper import check_access


class FarmList(Resource):
    @staticmethod
    @check_access([Roles.ADMIN, Roles.FARMER])
    def get():
        return jsonify(get_all_farms())


class FarmGet(Resource):

    @check_access([Roles.ADMIN, Roles.FARMER])
    def get(self, farm_id: int):
        return jsonify(query_farm_by_id(farm_id).first_or_404().serialize())

    @check_access([Roles.ADMIN])
    def post(self, farm_id: int):
        request_data = request.json
        farm = updateFarm(request_data)
        return {'msg': farm.serialize()}, HTTPStatus.OK if farm_id is not None else HTTPStatus.CREATED
