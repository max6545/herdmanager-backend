from flask import jsonify
from flask_restful import Resource
from app.model.animal import AnimalType
#from app.app import logger
class AnimalTypeList(Resource):
    @staticmethod
    def get():
        #logger.info('check animals')
        return jsonify([animal_type.name for animal_type in AnimalType])
