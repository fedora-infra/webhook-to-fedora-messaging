from webhook_to_fedora_messaging_messages.github import GitHubMessageV1

from ...fasjson import get_fasjson
from .base import BaseParser, Body, BodyData, HeadersDict


class GitHubParser(BaseParser):

    message_class = GitHubMessageV1

    async def validate(self, headers: HeadersDict, data: BodyData) -> None:
        """
        Verify that the payload was sent from GitHub by validating SHA256.
        """
        self._validate_with_sig_header(headers["x-hub-signature-256"], data)

    def _get_topic(self, headers: HeadersDict, body: Body) -> str:
        return f"github.{headers['x-github-event']}"

    async def _get_agent(self, body: Body) -> str | None:
        return await get_fasjson().get_username_from_github(body["sender"]["login"])
