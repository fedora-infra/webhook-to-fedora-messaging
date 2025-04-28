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
async def test_service_list(client, authenticated, db_service):
    """
    Listing all available services
    """
    response = await client.get("/api/v1/services")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "creation_date": db_service.creation_date.isoformat(),
                "desc": db_service.desc,
                "name": db_service.name,
                "token": db_service.token,
                "type": db_service.type,
                "uuid": db_service.uuid,
                "webhook_url": f"http://test/api/v1/messages/{db_service.uuid}",
            },
        ],
    }
