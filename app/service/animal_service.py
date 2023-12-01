from flask import jsonify, request
from flask_restful import Resource
from app.model.animal import HerdAnimalType, Animal
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.model.dao.animal_dao import get_herd_animals, get_other_animals, get_rejected_animals


class AnimalTypeList(Resource):
    @staticmethod
    def get():
        return jsonify([animal_type.name for animal_type in HerdAnimalType])


class AnimalList(Resource):
    @staticmethod
    @jwt_required()
    def get():
        list_type = request.args['type']
        user_id = get_jwt_identity()
        animal_list: list[Animal] = []
        match list_type:
            case 'herd':
                animal_list = get_herd_animals(user_id=user_id)
            case 'other':
                animal_list = get_other_animals(user_id=user_id)
            case 'rejected':
                animal_list = get_rejected_animals(user_id=user_id)
        return jsonify([animal.serialize() for animal in animal_list])
