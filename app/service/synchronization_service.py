from http import HTTPStatus

from flask import request
from flask_restful import Resource


class SynchronizeDB(Resource):
    @staticmethod
    #@jwt_required()
    def get():
        # method returns changes since last sync
        response = {
            'changes': [

            ],
            'timestamp': 1000
        }
        return response, HTTPStatus.OK

    @staticmethod
    #@jwt_required()
    def post():
        # methods synchronizes backendDB with clientDB with respect to incoming changes
        request.get_json(force=True)
        print(request.data)
        return None, HTTPStatus.NOT_FOUND
