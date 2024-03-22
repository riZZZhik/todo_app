def test_find_by_title(client) -> None:
    response = client.get("/tasks/find?title=yet another task")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_find_by_description(client) -> None:
    response = client.get("/tasks/find?description=yet another description")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_find_by_both(client) -> None:
    response = client.get(
        "/tasks/find?title=another task&description=another description"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2
