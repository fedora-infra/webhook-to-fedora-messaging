from httpx import AsyncClient

from webhook_to_fedora_messaging.models.user import User


async def test_user_search(client: AsyncClient, db_user: User) -> None:
    """
    Searching users with valid format
    """
    response = await client.get("/api/v1/users/search/met")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "creation_date": db_user.creation_date.isoformat(),
                "is_admin": False,
                "name": db_user.name,
            }
        ]
    }


async def test_user_search_too_short(client: AsyncClient, db_user: User) -> None:
    """
    Searching users with wrong format
    """
    response = await client.get("/api/v1/users/search/%20")
    assert response.status_code == 422
    assert response.json() == {"detail": "No lookup string provided"}
