import pytest


@pytest.mark.parametrize(
    "data, code",
    [
        pytest.param(
            {"username": "mehmet"},
            200,
            id="SERVICE Endpoint - 200 Success",
        ),
        pytest.param(
            {"username": "baran"},
            404,
            id="SERVICE Endpoint - 404 Not Found",
        ),
        pytest.param(
            {"user": "mehmet"},
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
def test_service_list(client, data, code):
    response = client.get("/service/search", json=data)
    assert response.status_code == code
