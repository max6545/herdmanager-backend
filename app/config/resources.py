from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api

from app.model.user import User
from app.service.admin_service import BackupDB, RestoreDB, CreateAdminUser
from app.service.animal_service import AnimalList
from app.service.auth_service import LoginApi, RefreshToken
from app.service.farm_service import FarmList, FarmGet
from app.service.synchronization_service import SynchronizeDB
from app.service.user_service import UserList, UserGet


def set_resources(_app):
    api = Api(_app)
    bcrypt = Bcrypt(_app)
    jwt = JWTManager(_app)

    api.add_resource(LoginApi, '/auth/login')
    api.add_resource(RefreshToken, '/auth/refresh')
    api.add_resource(UserGet, '/user/<user_id>')
    api.add_resource(UserList, '/user')
    api.add_resource(FarmGet, '/farm/<int:farm_id>')
    api.add_resource(FarmList, '/farm')
    api.add_resource(AnimalList, '/animal')
    api.add_resource(SynchronizeDB, '/synchronize')
    api.add_resource(BackupDB, '/admin/backupDB')
    api.add_resource(RestoreDB, '/admin/restoreDB')
    api.add_resource(CreateAdminUser, '/admin/createAdminUser')

    # here define callback function which returns current user model
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        """ callback for fetching authenticated user from db """
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()
