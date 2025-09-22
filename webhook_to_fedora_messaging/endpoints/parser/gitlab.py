from webhook_to_fedora_messaging_messages.gitlab import GitLabMessageV1

from ...fasjson import get_fasjson
from .base import BaseParser, Body, HeadersDict


class GitLabParser(BaseParser):

    message_class = GitLabMessageV1
    # Gitlab does not provide a SHA256 header for validation
    signature_header_name = None

    def _get_topic(self, headers: HeadersDict, body: Body) -> str:
        event = headers["x-gitlab-event"].replace(" Hook", "").replace(" ", "_").lower()
        return f"gitlab.{event}"

    async def _get_agent(self, body: Body) -> str | None:
        if body["object_kind"] == "push":
            username = body["user_username"]
        else:
            username = body["user"]["username"]
        return await get_fasjson().get_username("gitlab", username)
