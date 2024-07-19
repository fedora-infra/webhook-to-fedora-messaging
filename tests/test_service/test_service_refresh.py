import pytest


@pytest.mark.parametrize(
    "data, code",
    [
        pytest.param(
            {'service_uuid': 1,
             'username': 'mehmet'},
            200,
            id="SERVICE Endpoint - 200 Success",
        ),
        pytest.param(
            {"service_uuid": 2039,
             'username': "baran"},
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
@pytest.mark.usefixtures("create_service")
def test_service_refresh(client, data, code):
    response = client.post("/service/token", json=data)
    assert response.status_code == code
