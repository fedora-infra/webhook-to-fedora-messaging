from webhook_to_fedora_messaging_messages.forgejo import ForgejoMessageV1

from ...fasjson import get_fasjson
from .base import BaseParser, Body, HeadersDict


class ForgejoParser(BaseParser):
    message_class = ForgejoMessageV1
    signature_header_name = "x-hub-signature-256"

    def _get_topic(self, headers: HeadersDict, body: Body) -> str:
        return f"forgejo.{headers['x-forgejo-event']}"

    async def _get_agent(self, body: Body) -> str | None:
        # For action runs, use `run.trigger_user` instead of `sender`
        if "run" in body and "trigger_user" in body["run"]:
            return await get_fasjson().get_username("forgejo", body["run"]["trigger_user"]["login"])
        return await get_fasjson().get_username("forgejo", body["sender"]["login"])
