import pytest
from fastapi.testclient import TestClient

from settings import settings

settings.testing = True


@pytest.fixture()
def client():
    from some_stuff.main import app
    with TestClient(app) as rv:
        yield rv


@pytest.fixture()
def auth_client(client):
    client.headers[settings.api_key_name] = settings.api_key
