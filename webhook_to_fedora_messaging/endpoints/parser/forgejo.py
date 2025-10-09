from json import dumps, loads

from webhook_to_fedora_messaging_messages.forgejo import ForgejoMessageV1

from ...fasjson import get_fasjson
from .base import BaseParser, Body, HeadersDict


class ForgejoParser(BaseParser):
    message_class = ForgejoMessageV1
    signature_header_name = "x-hub-signature-256"

    def _get_topic(self, headers: HeadersDict, body: Body) -> str:
        return f"forgejo.{headers['x-forgejo-event']}"

    async def get_headers_and_data(self) -> tuple[HeadersDict, bytes]:
        headers = {k.lower(): v for k, v in self._request.headers.items()}
        data = await self._request.body()
        if "action_run" in headers["x-forgejo-event"]:
            info = loads(data.decode("utf-8"))["run"]["event_payload"]
            data = dumps(info).encode("utf-8")
        return headers, data

    async def _get_agent(self, body: Body) -> str | None:
        return await get_fasjson().get_username("forgejo", body["sender"]["login"])
