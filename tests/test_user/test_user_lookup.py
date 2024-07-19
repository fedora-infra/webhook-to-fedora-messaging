import pytest


@pytest.mark.parametrize(
    "data, code",
    [
        pytest.param(
            {"username": "mehmet"},
            200,
            id="USER Endpoint - 200 Success",
        ),
        pytest.param(
            {"username": "baran"},
            404,
            id="USER Endpoint - 404 Not Found",
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

@pytest.mark.usefixtures("create_user")
def test_user_lookup(client, data, code):
    response = client.get("/user/", json=data)
    assert response.status_code == code
    

@pytest.fixture
def create_user(client):
    data = {'username': 'mehmet'}
    client.post("/user/", json=data)
    
