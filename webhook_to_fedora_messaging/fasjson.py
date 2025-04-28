import logging
from functools import cache as ft_cache
from functools import cached_property as ft_cached_property
from typing import Any

import httpx
from cashews import cache
from httpx_gssapi import HTTPSPNEGOAuth

from .config import get_config


log = logging.getLogger(__name__)


class FASJSONAsyncProxy:
    """Proxy for the FASJSON API endpoints used in this app"""

    API_VERSION = "v1"

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=self.api_url, auth=HTTPSPNEGOAuth())

    @ft_cached_property
    def api_url(self) -> str:
        return f"{self.base_url.rstrip('/')}/{self.API_VERSION}"

    async def get(self, url: str, **kwargs) -> Any:
        """Query the API for a single result."""
        kwargs["follow_redirects"] = True
        response = await self.client.get(url, **kwargs)
        response.raise_for_status()
        return response.json()

    @cache(ttl="1d", prefix="v1")
    async def search_users(
        self,
        **params: dict[str, Any],
    ) -> list[dict]:
        return [user for user in (await self.get("/search/users/", params=params))["result"]]

    async def get_username_from_github(self, username):
        try:
            users = await self.search_users(github_username=username)
        except httpx.TimeoutException:
            log.exception("Timeout fetching the FAS user with Github username %r", username)
            return None
        if len(users) == 1:
            return users[0]["username"]
        return None

    async def get_username_from_forgejo(self, username):
        # TODO: Revisit user retrieval using FASJSON once the FAS supports Forgejo Auth
        return username


@ft_cache
def get_fasjson() -> FASJSONAsyncProxy:
    config = get_config()
    return FASJSONAsyncProxy(config.fasjson_url)
