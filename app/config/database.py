import os
from app.model.user import User


def initialize_db(_app, _db, _migrate):
    _db.init_app(_app)
    _migrate.init_app(_app,_db)
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
            # create new admin if default username/pw is changed and delete all users in db
            default_admin_users = User.query.filter_by(name='admin').first()
            if default_admin_users is not None:
                _db.session.delete(default_admin_users)
            user = User.create_user(username, password)
            _db.session.add(user)
            _db.session.commit()
            _app.logger.info('create default user{}'.format(username))
