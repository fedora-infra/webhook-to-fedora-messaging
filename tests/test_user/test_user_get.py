from unittest import mock

import pytest
from httpx import AsyncClient

from webhook_to_fedora_messaging.models.user import User


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
async def test_user_get(
    client: AsyncClient, authenticated: mock.MagicMock, db_user: User, username: str, code: int
) -> None:
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


async def test_user_get_me(
    client: AsyncClient, authenticated: mock.MagicMock, db_user: User
) -> None:
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
