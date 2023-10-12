from logging.config import dictConfig
from flask import Flask
from app.config.application import set_application_config
from app.config.database import initialize_db
from app.config.logging import logging_configuration
from app.config.resources import set_resources
from app.db.database import db
import logging
from flask_migrate import Migrate

# logging configuration
dictConfig(logging_configuration)

app = Flask(__name__)
set_application_config(app)
migrate = Migrate(app, db)
initialize_db(app, db, migrate)
set_resources(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
