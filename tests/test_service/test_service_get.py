import pytest


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
async def test_service_lookup(client, authenticated, db_service):
    """
    Spotting an existing service
    """
    response = await client.get(f"/api/v1/services/{db_service.uuid}")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "data": {
            "creation_date": db_service.creation_date.isoformat(),
            "desc": db_service.desc,
            "name": db_service.name,
            "token": db_service.token,
            "type": db_service.type,
            "uuid": db_service.uuid,
            "webhook_url": f"http://test/api/v1/messages/{db_service.uuid}",
        },
    }


async def test_service_404(client, authenticated):
    """
    Spotting a non-existent service
    """
    response = await client.get("/api/v1/services/not-existent-uuid")
    assert response.status_code == 404
