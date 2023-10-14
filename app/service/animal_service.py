from flask import jsonify
from flask_restful import Resource
from app.model.animal import AnimalType


class AnimalTypeList(Resource):
    @staticmethod
    def get():
        return jsonify([animal_type.name for animal_type in AnimalType])
