from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api
from app.service.backup_service import BackupDB
from app.service.animal_service import AnimalTypeList
from app.service.auth_service import SignupApi, LoginApi, RefreshToken
from app.service.synchronization_service import SynchronizeDB


def set_resources(_app):
    api = Api(_app)
    bcrypt = Bcrypt(_app)
    jwt = JWTManager(_app)

    api.add_resource(SignupApi, '/auth/signup')
    api.add_resource(LoginApi, '/auth/login')
    api.add_resource(RefreshToken, '/auth/refresh')

    api.add_resource(AnimalTypeList, '/animal/types')
    api.add_resource(SynchronizeDB, '/synchronize')
    api.add_resource(BackupDB, '/backup')
