from logging.config import dictConfig

from flask import Flask
from flask_cors import CORS

from app.config.application import set_application_config
from app.config.database import initialize_db
from app.config.logging import logging_configuration
from app.config.resources import set_resources

# logging configuration
dictConfig(logging_configuration)


def create_app(test: bool = False):
    app = Flask(__name__)
    set_application_config(app, test)
    with app.app_context():
        initialize_db(app, test)
    set_resources(app)
    CORS(app)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
