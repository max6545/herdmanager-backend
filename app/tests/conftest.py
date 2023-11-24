import pytest
from app.app import create_app
from flask.testing import FlaskClient


@pytest.fixture(scope='function')
def client(app):
    ctx = app.test_request_context()
    ctx.push()
    app.test_client_class = FlaskClient
    return app.test_client()


@pytest.fixture(scope='function')
def app():
    _app = create_app(True)
    with _app.app_context():
        yield _app


