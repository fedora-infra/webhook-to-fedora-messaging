from webhook_to_fedora_messaging_messages.gitlab import GitLabMessageV1

from ...fasjson import get_fasjson
from .base import BaseParser, Body, BodyData, HeadersDict


class GitLabParser(BaseParser):

    message_class = GitLabMessageV1

    async def get_headers_and_data(self) -> tuple[HeadersDict, bytes]:
        headers = {k.lower(): v for k, v in self._request.headers.items()}
        data = await self._request.body()
        return headers, data

    async def validate(self, headers: HeadersDict, data: BodyData) -> None:
        """
        Verify that the payload was sent from GitLab by validating SHA256.
        """

        # Gitlab does not provide a SHA256 header for validation
        pass

    def _get_topic(self, headers: HeadersDict, body: Body) -> str:
        event = headers["x-gitlab-event"].replace(" Hook", "").replace(" ", "_").lower()
        return f"gitlab.{event}"

    async def _get_agent(self, body: Body) -> str | None:
        if body["object_kind"] == "push":
            username = body["user_username"]
        else:
            username = body["user"]["username"]
        return await get_fasjson().get_username("gitlab", username)
