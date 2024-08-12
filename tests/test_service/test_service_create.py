import pytest


@pytest.mark.parametrize(
    "data, code",
    [
        pytest.param(
            {"type": "github", "desc": "Github Demo", "name": "My Github"},
            201,
            id="SERVICE Endpoint - 201 Created",
        ),
        pytest.param(
            {"type": "github", "desc": "Github Demo"},
            422,
            id="SERVICE Endpoint - 400 Bad Request",
        ),
    ],
)
@pytest.mark.usefixtures("db_user")
async def test_service_create(client, client_auth, data, code):
    response = await client.post("/api/v1/services", auth=client_auth, json={"data": data})
    assert response.status_code == code, response.text
    if code == 201:
        result = response.json()
        assert "data" in result
        for prop in ("type", "desc", "name"):
            assert result["data"][prop] == data[prop]


async def test_service_conflict(client, client_auth, db_service, db_user):
    data = {
        "name": db_service.name,
        "type": db_service.type,
        "desc": db_service.desc,
    }

    response = await client.post("/api/v1/services", auth=client_auth, json={"data": data})
    assert response.status_code == 409
