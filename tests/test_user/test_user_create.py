import pytest


@pytest.mark.parametrize(
    "data, code",
    [
        pytest.param(
            {"username": "mehmet"},
            201,
            id="USER Endpoint - 201 Created",
        ),
        pytest.param(
            {"username": "mehmet"},
            409,
            id="USER Endpoint - 409 Conflict",
        ),
        pytest.param(
            {"password": ""},
            400,
            id="USER Endpoint - 400 Bad Request"
        ),
        pytest.param(
            None,
            415,
            id="USER Endpoint - 415 Unsupported Media Type"
        )
    ]
)
def test_user_create(client, data, code):
    response = client.post("/user/", json=data)
    assert response.status_code == code
