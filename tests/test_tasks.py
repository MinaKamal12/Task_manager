import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite://"

from app.database import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task():
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Learn Docker", "description": "Containerize the API"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Learn Docker"
    assert data["description"] == "Containerize the API"
    assert data["completed"] is False
    assert "id" in data


def test_list_tasks():
    client.post("/api/v1/tasks", json={"title": "Task 1"})
    client.post("/api/v1/tasks", json={"title": "Task 2"})

    response = client.get("/api/v1/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task():
    created = client.post("/api/v1/tasks", json={"title": "Test task"}).json()

    response = client.get(f"/api/v1/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.json()["title"] == "Test task"


def test_update_task():
    created = client.post("/api/v1/tasks", json={"title": "Old title"}).json()

    response = client.put(
        f"/api/v1/tasks/{created['id']}",
        json={"title": "New title", "completed": True},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New title"
    assert data["completed"] is True


def test_delete_task():
    created = client.post("/api/v1/tasks", json={"title": "Delete me"}).json()

    response = client.delete(f"/api/v1/tasks/{created['id']}")
    assert response.status_code == 204

    response = client.get(f"/api/v1/tasks/{created['id']}")
    assert response.status_code == 404


def test_missing_task():
    response = client.get("/api/v1/tasks/99999")
    assert response.status_code == 404
