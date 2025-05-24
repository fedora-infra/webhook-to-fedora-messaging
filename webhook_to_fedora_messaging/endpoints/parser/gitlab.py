from webhook_to_fedora_messaging_messages.gitlab import GitLabMessageV1

from ...endpoints.parser.base import initialize_parser
from ...fasjson import get_fasjson


@initialize_parser(require_signature=False)
async def gitlab_parser(headers: dict, body: dict) -> GitLabMessageV1:
    """
    Convert request objects into desired Fedora Messaging format
    """
    topic = f"gitlab.{headers['x-gitlab-event']}"
    agent = await get_fasjson().get_username_from_gitlab(body["user"]["username"])
    return GitLabMessageV1(topic=topic, body={"body": body, "headers": headers, "agent": agent})
