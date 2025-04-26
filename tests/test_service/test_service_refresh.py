from unittest import mock

import pytest
from httpx import AsyncClient

from webhook_to_fedora_messaging.models.service import Service


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
async def test_service_refresh(
    client: AsyncClient, authenticated: mock.MagicMock, db_service: Service
) -> None:
    """
    Regenerating access token of an existing service
    """
    data = {"service_uuid": db_service.uuid}
    response = await client.put(f"/api/v1/services/{db_service.uuid}/regenerate", json=data)
    assert response.status_code == 202


async def test_service_refresh_404(client: AsyncClient, authenticated: mock.MagicMock) -> None:
    """
    Regenerating access token of a non-existent service
    """
    data = {"service_uuid": "not-existent-uuid"}
    response = await client.put("/api/v1/services/not-existent-uuid/regenerate", json=data)
    assert response.status_code == 404
