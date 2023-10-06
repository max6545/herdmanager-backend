from logging.config import dictConfig

from flask import Flask

from config.application import set_application_config
from config.database import initialize_db
from config.logging import logging_configuration
from config.resources import set_resources
from db.database import db

# logging configuration
dictConfig(logging_configuration)

app = Flask(__name__)
set_application_config(app)
initialize_db(app, db)
set_resources(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)