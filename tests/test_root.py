from httpx import AsyncClient


async def test_root_serves_ui(client: AsyncClient) -> None:
    """
    Serving UI from root endpoint
    """
    response = await client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
