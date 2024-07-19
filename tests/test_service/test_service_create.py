import pytest


@pytest.mark.parametrize(
    "data, code",
    [
        pytest.param(
            {"username": "mehmet",
             "type": "Github",
             "desc": "Github Demo",
             "name": "My Github"},
            201,
            id="SERVICE Endpoint - 201 Created",
        ),
        pytest.param(
            {"username": "baran",
             "type": "Github",
             "desc": "Github Demo",
             "name": "My Github"},
            404,
            id="SERVICE Endpoint - 404 Not Found",
        ),
        pytest.param(
            {"username": "mehmet",
             "type": "Github",
             "desc": "Github Demo"},
            400,
            id="SERVICE Endpoint - 400 Bad Request"
        ),
        pytest.param(
            None,
            415,
            id="SERVICE Endpoint - 415 Unsupported Media Type"
        )
    ]
)
@pytest.mark.usefixtures("create_user")
def test_service_create(client, data, code):
    response = client.post("/service/", json=data)
    assert response.status_code == code
    
@pytest.mark.parametrize(
    "data, code",
    [
        pytest.param(
            {"username": "mehmet",
             "type": "Github",
             "desc": "Github Demo",
             "name": "My Github"},
            409,
            id="SERVICE Endpoint - 409 Conflict",
        )
    ]
)
@pytest.mark.usefixtures("create_user")
def test_service_conflict(client, data, code):
    response = client.post("/service/", json=data)
    response = client.post("/service/", json=data)
    assert response.status_code == code
