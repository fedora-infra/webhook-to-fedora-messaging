async def test_service_lookup(client, client_auth, db_service):
    response = await client.get(f"/api/v1/services/{db_service.uuid}", auth=client_auth)
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "creation_date": db_service.creation_date.isoformat(),
            "desc": db_service.desc,
            "name": db_service.name,
            "token": db_service.token,
            "type": db_service.type,
            "user_id": db_service.user_id,
            "uuid": db_service.uuid,
        },
    }


async def test_service_404(client, client_auth):
    response = await client.get("/api/v1/services/not-existent-uuid", auth=client_auth)
    assert response.status_code == 404
