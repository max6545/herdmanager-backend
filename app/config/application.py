import os


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
        _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farminv.db'
    if 'JWT_KEY' in os.environ:
        _app.config['JWT_SECRET_KEY'] = os.getenv('JWT_KEY')
    else:
        _app.logger.warning('JWT_KEY not set. The application is insecure')
        _app.config['JWT_SECRET_KEY'] = 'insecureDefaultKey'
