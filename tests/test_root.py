from httpx import AsyncClient


async def test_root_redirect(client: AsyncClient) -> None:
    """
    Redirecting to API documentation
    """
    response = await client.get("/")
    assert response.status_code == 307
    assert response.headers.get("location") == "/docs"
