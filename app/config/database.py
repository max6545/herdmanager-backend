import os

from model.user import User


def initialize_db(_app, _db):
    _db.init_app(_app)
    with _app.app_context():
        _db.create_all()
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
            user = User.create_user(username, password)
            _db.session.add(user)
            _db.session.commit()
            _app.logger.info('create default user{}'.format(username))
