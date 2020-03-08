from unittest.mock import ANY

import pytest
from fastapi import status


def test_create_and_read(client, auth_client):
    response = client.post("/some-stuff/", json={"name": "Alice"})
    assert response.status_code == status.HTTP_201_CREATED
    response_body = response.json()
    assert response_body == {"id": ANY, "name": "Alice"}
    get_response = client.get(f"/some-stuff/{response_body['id']}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json() == response_body


def test_read_not_found(client, auth_client):
    response = client.get("/some-stuff/17")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_empty(client, auth_client):
    response = client.get("/some-stuff/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"items": [], "limit": 10, "offset": 0}


def test_list(client, auth_client):
    client.post("/some-stuff/", json={"name": "Alice"})
    client.post("/some-stuff/", json={"name": "Bob"})
    response = client.get("/some-stuff/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "items": [
            {
                "id": ANY,
                "name": "Alice",
            },
            {
                "id": ANY,
                "name": "Bob"
            },
        ],
        "limit": 10,
        "offset": 0,
    }


def test_list_pagination(client, auth_client):
    for x in range(10):
        client.post("/some-stuff/", json={"name": str(x)})
    response = client.get("/some-stuff/", params={"limit": 2, "offset": 3})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "items": [
            {
                "id": ANY,
                "name": "3",
            },
            {
                "id": ANY,
                "name": "4"
            },
        ],
        "limit": 2,
        "offset": 3,
    }


def test_list_pagination_over_limit(client, auth_client):
    for x in range(10):
        client.post("/some-stuff/", json={"name": str(x)})
    response = client.get("/some-stuff/", params={"limit": 2, "offset": 30})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "items": [],
        "limit": 2,
        "offset": 30,
    }


def test_list_by_name(client, auth_client):
    client.post("/some-stuff/", json={"name": "Alice"})
    client.post("/some-stuff/", json={"name": "Alice"})
    client.post("/some-stuff/", json={"name": "Bob"})
    response = client.get("/some-stuff/", params={"name": "Alice"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "items": [
            {
                "id": ANY,
                "name": "Alice",
            },
            {
                "id": ANY,
                "name": "Alice"
            },
        ],
        "limit": 10,
        "offset": 0,
    }


def test_list_by_name_pagination(client, auth_client):
    for x in range(10):
        for _ in range(3):
            client.post("/some-stuff/", json={"name": str(x)})
    response = client.get("/some-stuff/", params={"name": "1", "limit": 2, "offset": 2})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "items": [
            {
                "id": ANY,
                "name": "1",
            },
        ],
        "limit": 2,
        "offset": 2,
    }


def test_update_existent(client, auth_client):
    item_id = client.post("/some-stuff/", json={"name": "Alice"}).json()["id"]
    response = client.put(f"/some-stuff/{item_id}", json={"name": "Eva"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": item_id, "name": "Eva"}
    assert client.get(f"/some-stuff/{item_id}").json() == {"id": item_id, "name": "Eva"}


def test_update_not_found(client, auth_client):
    response = client.put("/some-stuff/17", json={"name": "Alice"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete(client, auth_client):
    item_id = client.post("/some-stuff/", json={"name": "Alice"}).json()["id"]
    assert client.get(f"/some-stuff/{item_id}").status_code == status.HTTP_200_OK
    response = client.delete(f"/some-stuff/{item_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert client.get(f"/some-stuff/{item_id}").status_code == status.HTTP_404_NOT_FOUND


def test_delete_not_existent_ok(client, auth_client):
    assert client.delete("/some-stuff/17").status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.parametrize("method, url", [
    ("get", "/some-stuff/"),
    ("post", "/some-stuff/"),
    ("get", "/some-stuff/1"),
    ("put", "/some-stuff/1"),
    ("delete", "/some-stuff/1"),
])
def test_not_authorized_client_get_403(client, method, url):
    response = client.request(method, url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
