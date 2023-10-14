import os
import nextcloud_client


def set_application_config(_app):
    _app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # check mysql_config and set passed value
    if 'MYSQL_CONNECTION_STRING' in os.environ:
        _app.logger.info('Application using MYSQL DB')
        mysql_connection_string = os.getenv('MYSQL_CONNECTION_STRING')
        _app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://' + mysql_connection_string
    # if no mysql_config is set -> sqlite
    else:
        _app.logger.info('Application using SQLite DB')
        if 'IN_DOCKER_ENV' in os.environ:
            get_latest_nc_backup(_app)
        _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farminv.db'
    if 'JWT_KEY' in os.environ:
        _app.config['JWT_SECRET_KEY'] = os.getenv('JWT_KEY')
    else:
        _app.logger.warning('JWT_KEY not set. The application is insecure')
        _app.config['JWT_SECRET_KEY'] = 'insecureDefaultKey'


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
            _app.logger.info(f'fetch last backup in list[{backup_list[-1]}]')
            backup_dir = '/usr/local/var/app.app-instance'
            os.mkdir(backup_dir)
            nc.get_file(backup_list[-1].path, backup_dir + '/farminv.db')
    except:
        _app.logger.error('Cant fetch last backup')
