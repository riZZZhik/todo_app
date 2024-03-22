from datetime import datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.database import TasksDatabase
from app.models import Task

from .data import TEST_TASKS


@pytest.fixture
def app() -> FastAPI:
    from app.main import get_application  # local import for testing purpose

    return get_application()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_database() -> None:
    db = TasksDatabase("tasks.db")
    db._clear_tasks_table()

    for task in TEST_TASKS:
        db.create_task(
            Task(**task, created_at=str(datetime.now()), updated_at=str(datetime.now()))
        )
