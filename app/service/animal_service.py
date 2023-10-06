from flask import jsonify
from flask_restful import Resource
from db.database import db
from model.animal import AnimalType, Animal


class AnimalTypeList(Resource):
    @staticmethod
    def get():
        animal = Animal(name='Test')
        db.session.add(animal)
        db.session.commit()

        return jsonify([animal_type.name for animal_type in AnimalType])


