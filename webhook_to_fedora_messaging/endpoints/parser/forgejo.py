from webhook_to_fedora_messaging_messages.forgejo import ForgejoMessageV1

from ...fasjson import get_fasjson
from .base import BaseParser, Body, HeadersDict


class ForgejoParser(BaseParser):
    message_class = ForgejoMessageV1
    signature_header_name = "x-hub-signature-256"

    def _get_topic(self, headers: HeadersDict, body: Body) -> str:
        return f"forgejo.{headers['x-forgejo-event']}"

    async def _get_agent(self, body: Body) -> str | None:
        if "trigger_user" in body:  # For action runs, use `trigger_user` instead of `sender`
            return await get_fasjson().get_username("forgejo", body["trigger_user"]["login"])
        return await get_fasjson().get_username("forgejo", body["sender"]["login"])
