import pytest

from app.main import flask_app


@pytest.fixture
def client():
    with flask_app.app.test_client() as client:
        yield client
