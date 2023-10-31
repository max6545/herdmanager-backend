import os
from app.model.user import User
import nextcloud_client

def initialize_db(_app, _db, _migrate):
    if 'IN_DOCKER_ENV' in os.environ:
        get_latest_nc_backup(_app)

    _db.init_app(_app)
    _migrate.init_app(_app, _db)
    with _app.app_context():
        if 'DEFAULT_USERNAME' in os.environ and 'DEFAULT_PASSWORD' in os.environ:
            username = os.getenv('DEFAULT_USERNAME')
            password = os.getenv('DEFAULT_PASSWORD')
        else:
            _app.logger.warning('Variable for DEFAULT_USERNAME and DEFAULT_PASSWORD '
                                'not set using credentials admin:admin')
            username = 'admin'
            password = 'admin'
        user = User.query.filter_by(name=username).first()
        if user is None:
            # create new admin if default username/pw is changed and delete all users in db
            default_admin_users = User.query.filter_by(name='admin').first()
            if default_admin_users is not None:
                _db.session.delete(default_admin_users)
            user = User.create_user(username, password)
            _db.session.add(user)
            _db.session.commit()
            _app.logger.info(f'create default user [{username}]')
        else:
            _app.logger.info(f'defaultuser already exists [{username}]')


def get_latest_nc_backup(_app):
    _app.logger.info('start fetching backup')
    nc = nextcloud_client.Client(os.environ.get('NEXTCLOUD_HOST'))
    nc.login(os.environ.get('NEXTCLOUD_USER'), os.environ.get('NEXTCLOUD_PASSWORD'))
    backup_dir = 'farminv-backup-server'
    try:
        backup_list = nc.list(backup_dir)
        if len(backup_list) == 0:
            _app.logger.info('no backup exists create new db on gunicorn start')
        else:
            _app.logger.info(f'fetch last backup in list[{backup_list[-1].path}]')
            backup_dir = '/usr/local/var/app.app-instance'
            os.makedirs(backup_dir)
            nc.get_file(backup_list[-1].path, backup_dir + '/farminv.db')
        _app.logger.info(f'fetch db ok')
    except:
        _app.logger.error('Cant fetch last backup')
