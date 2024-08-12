async def test_user_search(client, client_auth, db_user):
    response = await client.get("/api/v1/users/search/met", auth=client_auth)
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "creation_date": db_user.creation_date.isoformat(),
                "is_admin": False,
                "name": db_user.name,
                "uuid": db_user.uuid,
            }
        ]
    }
