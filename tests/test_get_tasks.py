def test_get_tasks_top_n(client) -> None:
    response = client.get("/tasks/?top_n=1")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_get_tasks_sort_by_title(client) -> None:
    response = client.get("/tasks/?sort_by=title")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    titles = [task["title"] for task in response.json()]
    assert titles == sorted(titles)


def test_get_tasks_sort_by_status(client) -> None:
    response = client.get("/tasks/?sort_by=status")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    statuses = [task["status"] for task in response.json()]
    assert statuses == sorted(statuses, reverse=True)


def test_get_tasks_sort_by_priority(client) -> None:
    response = client.get("/tasks/?sort_by=priority")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    priorities = [task["priority"] for task in response.json()]
    assert priorities == sorted(priorities, reverse=True)


def test_get_tasks_sort_by_created_at(client) -> None:
    response = client.get("/tasks/?sort_by=created_at")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    created_at = [task["created_at"] for task in response.json()]
    assert created_at == sorted(created_at)


def test_get_tasks_sort_by_updated_at(client) -> None:
    response = client.get("/tasks/?sort_by=updated_at")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    updated_at = [task["updated_at"] for task in response.json()]
    assert updated_at == sorted(updated_at)
