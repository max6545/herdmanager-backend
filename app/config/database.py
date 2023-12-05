def initialize_db(_app, _db, _migrate, test: bool = False):
    _db.init_app(_app)
    _migrate.init_app(_app, _db)
    if test:
        _db.create_all()
