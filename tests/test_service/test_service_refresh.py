async def test_service_refresh(client, client_auth, db_service):
    data = {"service_uuid": db_service.uuid}
    response = await client.put(
        f"/api/v1/services/{db_service.uuid}/regenerate", auth=client_auth, json=data
    )
    assert response.status_code == 202


async def test_service_refresh_404(client, client_auth):
    data = {"service_uuid": "not-existent-uuid"}
    response = await client.put(
        "/api/v1/services/not-existent-uuid/regenerate", auth=client_auth, json=data
    )
    assert response.status_code == 404
