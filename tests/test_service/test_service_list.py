async def test_service_list(client, client_auth, db_service):
    response = await client.get("/api/v1/services", auth=client_auth)
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "creation_date": db_service.creation_date.isoformat(),
                "desc": db_service.desc,
                "name": db_service.name,
                "token": db_service.token,
                "type": db_service.type,
                "user_id": db_service.user_id,
                "uuid": db_service.uuid,
            },
        ],
    }
