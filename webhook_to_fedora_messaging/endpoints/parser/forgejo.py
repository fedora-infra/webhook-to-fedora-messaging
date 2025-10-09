import json

from fedora_messaging.api import Message
from webhook_to_fedora_messaging_messages.forgejo import ForgejoMessageV1

from ...fasjson import get_fasjson
from .base import BaseParser, Body, HeadersDict


class ForgejoParser(BaseParser):
    message_class = ForgejoMessageV1
    signature_header_name = "x-hub-signature-256"

    def _get_topic(self, headers: HeadersDict, body: Body) -> str:
        return f"forgejo.{headers['x-forgejo-event']}"

    async def parse(self) -> Message:
        headers, data = await self.get_headers_and_data()

        if self._token:
            await self.validate(headers, data)

        if "action_run" in headers.get("x-forgejo-event", ""):
            info = json.loads(data.decode("utf-8"))["run"]["event_payload"]
            data = info.encode("utf-8")

        body = json.loads(data.decode("utf-8"))
        topic = self._get_topic(headers, body)
        agent = await self._get_agent(body)
        return self.message_class(
            topic=topic, body={"body": body, "headers": headers, "agent": agent}
        )

    async def _get_agent(self, body: Body) -> str | None:
        return await get_fasjson().get_username("forgejo", body["sender"]["login"])
