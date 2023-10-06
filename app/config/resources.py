from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api

from service.animal_service import AnimalTypeList
from service.auth_service import SignupApi, LoginApi
from service.synchronization_service import SynchronizeDB


def set_resources(_app):
    api = Api(_app)
    bcrypt = Bcrypt(_app)
    jwt = JWTManager(_app)

    api.add_resource(SignupApi, '/auth/signup')
    api.add_resource(LoginApi, '/auth/login')
    api.add_resource(AnimalTypeList, '/animal/types')
    #api.add_resource(AnimalList, '/sheep/list')
    #api.add_resource(SheepService, '/sheep/<sheep_id>')
    #api.add_resource(SheepAdd, '/sheep')
    api.add_resource(SynchronizeDB, '/synchronize')
