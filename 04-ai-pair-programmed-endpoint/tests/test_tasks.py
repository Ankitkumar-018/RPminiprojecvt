import pytest
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app import app, tasks


@pytest.fixture(autouse=True)
def clear_tasks():
    tasks.clear()
    yield
    tasks.clear()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ── List Tasks ───────────────────────────────────────────────

def test_list_tasks_empty(client):
    res = client.get("/tasks")
    assert res.status_code == 200
    data = res.get_json()
    assert data["tasks"] == []
    assert data["count"] == 0


def test_list_tasks_returns_all(client):
    client.post("/tasks", json={"title": "Task A"})
    client.post("/tasks", json={"title": "Task B"})
    res = client.get("/tasks")
    assert res.get_json()["count"] == 2


def test_list_tasks_filter_by_completed(client):
    client.post("/tasks", json={"title": "Task A"})
    res_create = client.post("/tasks", json={"title": "Task B"})
    task_id = res_create.get_json()["id"]
    client.patch(f"/tasks/{task_id}", json={"completed": True})

    res = client.get("/tasks?completed=true")
    data = res.get_json()
    assert data["count"] == 1
    assert data["tasks"][0]["title"] == "Task B"


def test_list_tasks_filter_by_priority(client):
    client.post("/tasks", json={"title": "High task", "priority": "high"})
    client.post("/tasks", json={"title": "Low task", "priority": "low"})

    res = client.get("/tasks?priority=high")
    data = res.get_json()
    assert data["count"] == 1
    assert data["tasks"][0]["title"] == "High task"


# ── Create Task ──────────────────────────────────────────────

def test_create_task_success(client):
    res = client.post("/tasks", json={"title": "Buy groceries", "priority": "high"})
    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == "Buy groceries"
    assert data["priority"] == "high"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data


def test_create_task_default_priority(client):
    res = client.post("/tasks", json={"title": "Simple task"})
    assert res.status_code == 201
    assert res.get_json()["priority"] == "medium"


def test_create_task_missing_title(client):
    res = client.post("/tasks", json={"description": "No title here"})
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_create_task_empty_title(client):
    res = client.post("/tasks", json={"title": "   "})
    assert res.status_code == 400


def test_create_task_invalid_priority(client):
    res = client.post("/tasks", json={"title": "Task", "priority": "urgent"})
    assert res.status_code == 400


def test_create_task_no_body(client):
    res = client.post("/tasks", content_type="application/json", data="")
    assert res.status_code == 400


# ── Get Single Task ──────────────────────────────────────────

def test_get_task_success(client):
    created = client.post("/tasks", json={"title": "Read book"}).get_json()
    res = client.get(f"/tasks/{created['id']}")
    assert res.status_code == 200
    assert res.get_json()["title"] == "Read book"


def test_get_task_not_found(client):
    res = client.get("/tasks/nonexistent-id")
    assert res.status_code == 404


# ── Update Task ──────────────────────────────────────────────

def test_update_task_title(client):
    created = client.post("/tasks", json={"title": "Old title"}).get_json()
    res = client.patch(f"/tasks/{created['id']}", json={"title": "New title"})
    assert res.status_code == 200
    assert res.get_json()["title"] == "New title"


def test_update_task_mark_completed(client):
    created = client.post("/tasks", json={"title": "Finish project"}).get_json()
    res = client.patch(f"/tasks/{created['id']}", json={"completed": True})
    assert res.status_code == 200
    assert res.get_json()["completed"] is True


def test_update_task_invalid_completed_type(client):
    created = client.post("/tasks", json={"title": "Task"}).get_json()
    res = client.patch(f"/tasks/{created['id']}", json={"completed": "yes"})
    assert res.status_code == 400


def test_update_task_not_found(client):
    res = client.patch("/tasks/bad-id", json={"title": "Whatever"})
    assert res.status_code == 404


# ── Delete Task ──────────────────────────────────────────────

def test_delete_task_success(client):
    created = client.post("/tasks", json={"title": "Delete me"}).get_json()
    res = client.delete(f"/tasks/{created['id']}")
    assert res.status_code == 200
    assert "deleted" in res.get_json()["message"]

    get_res = client.get(f"/tasks/{created['id']}")
    assert get_res.status_code == 404


def test_delete_task_not_found(client):
    res = client.delete("/tasks/ghost-id")
    assert res.status_code == 404


# ── Stats ────────────────────────────────────────────────────

def test_stats_empty(client):
    res = client.get("/tasks/stats")
    assert res.status_code == 200
    data = res.get_json()
    assert data["total"] == 0
    assert data["completed"] == 0
    assert data["pending"] == 0


def test_stats_with_data(client):
    res1 = client.post("/tasks", json={"title": "T1", "priority": "high"}).get_json()
    client.post("/tasks", json={"title": "T2", "priority": "low"})
    client.patch(f"/tasks/{res1['id']}", json={"completed": True})

    res = client.get("/tasks/stats")
    data = res.get_json()
    assert data["total"] == 2
    assert data["completed"] == 1
    assert data["pending"] == 1
    assert data["by_priority"]["high"] == 1
    assert data["by_priority"]["low"] == 1
