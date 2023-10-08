from flask import jsonify
from flask_restful import Resource
from db.database import db
from model.animal import AnimalType, Animal
import time

class AnimalTypeList(Resource):
    @staticmethod
    def get():
        return jsonify([animal_type.name for animal_type in AnimalType])


