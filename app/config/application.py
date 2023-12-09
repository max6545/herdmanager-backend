import os
from urllib.parse import quote


def set_application_config(_app, test: bool = False):
    with _app.app_context():
        _app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        # check mysql_config and set passed value
        if test:
            db_name = "farminv-test.db"
            db_path = f"{os.pardir}/instance/{db_name}"
            _app.config['JWT_HEADER_TYPE'] = 'Bearer'
            _app.config['JWT_BLACKLIST_ENABLED'] = False
            if os.path.isfile(db_path):
                _app.logger.debug(f'Delete exsting db {db_name}')
                os.remove(db_path)
            _app.logger.info('Application using SQLite DB for TESTS')
            _app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'

        else:
            if 'USE_PG_DB' in os.environ:
                _app.logger.info('Application using EXTERNAL_DB')
                pw = quote(os.getenv('DB_PW'))
                user = quote(os.getenv('DB_USER'))
                host = quote(os.getenv('DB_HOST'))
                db_name = quote(os.getenv('DB_NAME'))
                _app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{user}:{pw}@{host}/{db_name}'
            else:
                _app.logger.info('Application using SQLite DB')
                _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farminv.db'
        if 'JWT_KEY' in os.environ:
            _app.config['JWT_SECRET_KEY'] = os.getenv('JWT_KEY')
        else:
            _app.logger.warning('JWT_KEY not set. The application is insecure')
            _app.config['JWT_SECRET_KEY'] = 'insecureDefaultKey'
