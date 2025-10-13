from webhook_to_fedora_messaging_messages.github import GitHubMessageV1

from ...fasjson import get_fasjson
from .base import BaseParser, Body, HeadersDict


class GitHubParser(BaseParser):
    message_class = GitHubMessageV1
    signature_header_name = "x-hub-signature-256"

    def _get_topic(self, headers: HeadersDict, body: Body) -> str:
        return f"github.{headers['x-github-event']}"

    async def _get_agent(self, body: Body) -> str | None:
        return await get_fasjson().get_username("github", body["sender"]["login"])
