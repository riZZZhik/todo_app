import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def app() -> FastAPI:
    from app.main import get_application  # local import for testing purpose

    return get_application()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
