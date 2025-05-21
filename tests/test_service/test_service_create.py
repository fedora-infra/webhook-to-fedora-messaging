from unittest import mock

import pytest
from httpx import AsyncClient

from webhook_to_fedora_messaging.models.service import Service
from webhook_to_fedora_messaging.models.user import User


@pytest.mark.parametrize(
    "data, code",
    [
        pytest.param(
            {"type": "github", "desc": "GitHub Demo", "name": "My GitHub"},
            201,
            id="GitHub",
        ),
        pytest.param(
            {"type": "github", "desc": "GitHub Demo"},
            422,
            id="GitHub",
        ),
        pytest.param(
            {"type": "forgejo", "desc": "Forgejo Demo", "name": "My Forgejo"},
            201,
            id="Forgejo",
        ),
        pytest.param(
            {"type": "forgejo", "desc": "Forgejo Demo"},
            422,
            id="Forgejo",
        ),
    ],
)
async def test_service_create(
    client: AsyncClient, authenticated: mock.MagicMock, data: dict, code: int
) -> None:
    """
    Creating a non-existent service with wrong information
    """
    response = await client.post("/api/v1/services", json={"data": data})
    assert response.status_code == code, response.text
    if code == 201:
        result = response.json()
        assert "data" in result
        for prop in ("type", "desc", "name"):
            assert result["data"][prop] == data[prop]


@pytest.mark.parametrize(
    "db_service",
    [
        pytest.param(
            "github",
            id="GitHub",
        ),
        pytest.param(
            "forgejo",
            id="Forgejo",
        ),
    ],
    indirect=["db_service"],
)
async def test_service_conflict(
    client: AsyncClient, authenticated: mock.MagicMock, db_service: Service, db_user: User
) -> None:
    """
    Creating an existing service again
    """
    data = {
        "name": db_service.name,
        "type": db_service.type,
        "desc": db_service.desc,
    }
    response = await client.post("/api/v1/services", json={"data": data})
    assert response.status_code == 409, response.text
    assert response.json() == {"detail": "This service already exists"}
