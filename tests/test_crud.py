def test_create_task(client) -> None:
    response = client.post(
        "/tasks/",
        json={"title": "test task", "description": "test description"},
    )
    assert response.status_code == 201
    assert response.json()["title"] == "test task"
    assert response.json()["description"] == "test description"


def test_get_task(client) -> None:
    response = client.get("/tasks/1")

    assert response.status_code == 200
    assert response.json()["task_id"] == 1
    assert response.json()["title"] == "test task"
    assert response.json()["description"] == "test description"
    assert "created_at" in response.json()
    assert "updated_at" in response.json()


def test_get_task_not_found(client) -> None:
    response = client.get("/tasks/-1")

    assert response.status_code == 404
    assert response.json()["errors"] = ["Task not found"]


def test_get_tasks(client) -> None:
    response = client.get("/tasks/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    for task in response.json():
        assert "task_id" in task
        assert "title" in task
        assert "description" in task
        assert "status" in task
        assert "priority" in task
        assert "created_at" in task
        assert "updated_at" in task
    task_ids = [task["task_id"] for task in response.json()]
    assert task_ids == sorted(task_ids, reverse=True)


def test_update_task(client) -> None:
    response = client.put(
        "/tasks/1",
        json={"title": "updated task", "description": "updated description"},
    )

    assert response.status_code == 202
    assert response.json()["task_id"] == 1
    assert response.json()["title"] == "updated task"
    assert response.json()["description"] == "updated description"
    assert response.json()["updated_at"] != response.json()["created_at"]

def test_update_task_not_found(client) -> None:
    respose = client.put(
        "/tasks/-1",
        json={"title": "updated task", "description": "updated description"},
    )

    assert response.status_code == 404
    assert response.json()["errors"] == ["Task not found"]


def test_delete_task(client) -> None:
    response = client.delete("/tasks/1")

    assert response.status_code == 200
    response = client.get("/tasks/1")
    assert response.status_code == 404
    assert response.json() == {"errors": ["Task not found"]}
