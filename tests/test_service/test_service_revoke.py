async def test_service_revoke(client, client_auth, db_service):
    response = await client.put(f"/api/v1/services/{db_service.uuid}/revoke", auth=client_auth)
    assert response.status_code == 202


async def test_service_revoke_404(client, client_auth, db_service):
    response = await client.put("/api/v1/services/non-existent-uuid/revoke", auth=client_auth)
    assert response.status_code == 404
