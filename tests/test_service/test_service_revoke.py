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
            id="Forgejo - Revoking an existing service",
        ),
    ],
    indirect=["db_service"],
)
async def test_service_revoke(
    client: AsyncClient, authenticated: mock.MagicMock, db_service: Service
) -> None:
    """
    Revoking an existing service
    """
    response = await client.put(f"/api/v1/services/{db_service.uuid}/revoke")
    assert response.status_code == 202


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
async def test_service_revoke_404(
    client: AsyncClient, authenticated: mock.MagicMock, db_service: Service
) -> None:
    """
    Revoking a non-existent service
    """
    response = await client.put("/api/v1/services/non-existent-uuid/revoke")
    assert response.status_code == 404
