import logging
from functools import cache as ft_cache
from functools import cached_property as ft_cached_property
from typing import Any, cast

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

    async def get(self, url: str, **kwargs: Any) -> Any:
        """Query the API for a single result."""
        kwargs["follow_redirects"] = True
        response = await self.client.get(url, **kwargs)
        response.raise_for_status()
        return response.json()

    @cache(ttl="1d", prefix="v1")
    async def search_users(
        self,
        **params: Any,
    ) -> list[dict[str, Any]]:
        return [user for user in (await self.get("/search/users/", params=params))["result"]]

    async def _search_user(self, **filters: str) -> str | None:
        try:
            users = await self.search_users(**filters)
        except httpx.TimeoutException:
            log.exception("Timeout fetching the FAS user with %r", filters)
            return None
        if len(users) == 1:
            return cast(str, users[0]["username"])
        elif len(users) > 1:
            log.exception("Found multiple FAS users with %r", filters)
        return None

    async def get_username(self, service: str, username: str) -> str | None:
        if service == "forgejo":
            # Skip because FAS does not support Forgejo Auth yet
            return None
        if service == "github" and username.endswith("[bot]"):
            # Github bots can't be FAS users, skip them
            return None

        key = f"{service}_username"
        return await self._search_user(**{key: username})


@ft_cache
def get_fasjson() -> FASJSONAsyncProxy:
    config = get_config()
    return FASJSONAsyncProxy(config.fasjson_url)
