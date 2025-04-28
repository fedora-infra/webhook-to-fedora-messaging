import pytest


@pytest.mark.parametrize(
    "username, code",
    [
        pytest.param(
            "mehmet",
            200,
            id="General - Spotting an existing service",
        ),
        pytest.param(
            "baran",
            404,
            id="General - Spotting a non-existent service",
        ),
    ],
)
async def test_user_get(client, authenticated, db_user, username, code):
    """
    Spotting users
    """
    response = await client.get(f"/api/v1/users/{username}")
    assert response.status_code == code
    if code == 200:
        assert response.json() == {
            "data": {
                "creation_date": db_user.creation_date.isoformat(),
                "is_admin": False,
                "name": db_user.name,
            },
        }


async def test_user_get_me(client, authenticated, db_user):
    """
    Spotting myself
    """
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "creation_date": db_user.creation_date.isoformat(),
            "is_admin": False,
            "name": db_user.name,
        },
    }
