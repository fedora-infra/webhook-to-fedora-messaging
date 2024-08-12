async def test_service_update(client, client_auth, db_service, db_session):
    data = {"name": "new name"}
    response = await client.put(
        f"/api/v1/services/{db_service.uuid}", auth=client_auth, json={"data": data}
    )
    assert response.status_code == 202, response.text
    assert response.json()["data"]["name"] == "new name"
    await db_session.refresh(db_service)
    assert db_service.name == "new name"


async def test_service_update_404(client, client_auth):
    data = {"name": "new name"}
    response = await client.put(
        "/api/v1/services/non-existent-uuid", auth=client_auth, json={"data": data}
    )
    assert response.status_code == 404


async def test_service_update_bad_request(client, client_auth, db_service):
    data = {"something-else": "extra attr"}
    response = await client.put(
        f"/api/v1/services/{db_service.uuid}", auth=client_auth, json={"data": data}
    )
    assert response.status_code == 422
