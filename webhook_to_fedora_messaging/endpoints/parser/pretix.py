import logging
from typing import Any, cast

import httpx
from pydantic import BaseModel
from webhook_to_fedora_messaging_messages import PretixMessageV1

from ...config import get_config
from ...fasjson import get_fasjson
from .base import BaseParser, Body, HeadersDict

log = logging.getLogger(__name__)


class Attendee(BaseModel):
    name: str
    email: str


class PretixParser(BaseParser):
    message_class = PretixMessageV1

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._config = get_config().pretix
        self.http = httpx.AsyncClient(
            base_url=f"{self._config.url}/api",
            headers={"Authorization": f"Token {self._config.token}"},
        )

    def _get_topic(self, headers: HeadersDict, body: Body) -> str:
        return cast(str, body["action"])

    async def _get_attendee(self, body: Body) -> Attendee | None:
        """Get the attendee from the order."""
        if not body.get("code"):
            return None
        try:
            url = (
                f"/v1/organizers/{body['organizer']}/events/{body['event']}/orders/{body['code']}/"
            )
        except KeyError:
            log.exception("Unexpected pretix webhook: %s", repr(body))
            return None
        order_response = await self.http.get(url, follow_redirects=True)
        try:
            order_response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            log.error("Could not get the order from Pretix (%s): %s", url, exc)
            return None
        order = order_response.json()
        try:
            positionid = body["orderposition_positionid"] - 1
            name = order["positions"][positionid]["attendee_name"]
            email = order["positions"][positionid]["attendee_email"]
        except (KeyError, IndexError):
            log.info(
                "Pretix: position ID not found in order %s for webhook %s", repr(order), repr(body)
            )
            # Don't use order["email"], that's the customer's email.
            return None
        return Attendee(name=name, email=email)

    async def _get_agent_from_attendee(self, attendee: Attendee | None) -> str | None:
        if not attendee:
            return None
        if attendee.email.endswith(f"@{self._config.email_domain}"):
            return attendee.email.split("@", 1)[0]
        return await get_fasjson().get_username_from_email(attendee.email)

    async def _get_message_body(
        self, body: dict[str, Any], headers: HeadersDict, agent: str | None
    ) -> dict[str, Any]:
        message_body = await super()._get_message_body(body, headers, agent)
        message_body["body"]["instance_url"] = self._config.url
        # Attendee & agent
        attendee = await self._get_attendee(body)
        message_body["agent"] = await self._get_agent_from_attendee(attendee)
        message_body["body"]["attendee_name"] = attendee.name if attendee else None
        # Filter useless infra headers
        message_body["headers"] = {
            k: v for k, v in message_body["headers"].items() if "forwarded" not in k
        }
        return message_body
