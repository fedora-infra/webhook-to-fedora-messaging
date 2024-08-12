import pytest


@pytest.mark.parametrize(
    "username, code",
    [
        pytest.param(
            "mehmet",
            200,
            id="USER Endpoint - 200 Success",
        ),
        pytest.param(
            "baran",
            404,
            id="USER Endpoint - 404 Not Found",
        ),
    ],
)
async def test_user_get(client, client_auth, db_user, username, code):
    response = await client.get(f"/api/v1/users/{username}", auth=client_auth)
    assert response.status_code == code
    if code == 200:
        assert response.json() == {
            "data": {
                "creation_date": db_user.creation_date.isoformat(),
                "is_admin": False,
                "name": db_user.name,
                "uuid": db_user.uuid,
            },
        }
