from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api
from app.service.backup_service import BackupDB
from app.service.animal_service import AnimalTypeList, AnimalList
from app.service.auth_service import SignupApi, LoginApi, RefreshToken
from app.service.synchronization_service import SynchronizeDB
from app.service.user_service import UserList, UserGet
from app.service.farm_service import FarmList, FarmGet


def set_resources(_app):
    api = Api(_app)
    bcrypt = Bcrypt(_app)
    jwt = JWTManager(_app)

    api.add_resource(SignupApi, '/auth/signup')
    api.add_resource(LoginApi, '/auth/login')
    api.add_resource(RefreshToken, '/auth/refresh')
    api.add_resource(UserGet, '/user')
    api.add_resource(UserList, '/users')
    api.add_resource(FarmGet, '/farm')
    api.add_resource(FarmList, '/farms')
    api.add_resource(AnimalList, '/animal')
    api.add_resource(SynchronizeDB, '/synchronize')
    api.add_resource(BackupDB, '/backup')
