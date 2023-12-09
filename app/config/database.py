import logging
import os

from flask_migrate import Migrate

from app.db.database import db
from app.db.backup_management import get_latest_nc_backup
from app.model.farm import Farm
from app.model.user import User



def initialize_db(_app, test: bool = False):
    if 'IN_DOCKER_ENV' in os.environ:
        get_latest_nc_backup(_app)

    migrate = Migrate(_app, db)
    db.init_app(_app)
    migrate.init_app(_app, db)
    if test:
        db.create_all()
        create_initial_user()


def create_initial_user():
    if 'DEFAULT_USERNAME' in os.environ and 'DEFAULT_PASSWORD' in os.environ:
        username = os.getenv('DEFAULT_USERNAME')
        password = os.getenv('DEFAULT_PASSWORD')
    else:
        logging.warning('Variable for DEFAULT_USERNAME and DEFAULT_PASSWORD not set using credentials admin:admin')
        username = 'admin'
        password = 'admin'
    user = User.query.filter_by(name=username).one_or_none()
    
    if user is None:
        # create new admin if default username/pw is changed and delete all users in db
        default_admin_users = User.query.filter_by(name='admin').first()
        if default_admin_users is not None:
            db.session.delete(default_admin_users)
        user = User.create_user(username, password)
        user.roles = ['admin', 'farmer']
        farm = Farm()
        farm.name = 'TestFarm'
        db.session.add(farm)
        db.session.commit()
        user.farm_id = farm.id
        db.session.add(user)
        db.session.commit()
        message = f'create default user [{username}]'
    else:
        message = f'defaultuser already exists [{username}]'
    return message
