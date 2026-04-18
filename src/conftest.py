import pytest
from fastapi.testclient import TestClient

from fast_api import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app=app, raise_server_exceptions=False)
