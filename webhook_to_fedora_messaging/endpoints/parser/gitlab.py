from webhook_to_fedora_messaging_messages.gitlab import GitLabMessageV1

from ...endpoints.parser.base import initialize_parser
from ...fasjson import get_fasjson


@initialize_parser(require_signature=False)
async def gitlab_parser(headers: dict, body: dict) -> GitLabMessageV1:
    """
    Convert request objects into desired Fedora Messaging format
    """
    event = headers["x-gitlab-event"].replace(" Hook", "").replace(" ", "_").lower()
    topic = f"gitlab.{event}"
    if event == "push":
        agent = await get_fasjson().get_username_from_gitlab(body["user_username"])
    else:
        agent = await get_fasjson().get_username_from_gitlab(body["user"]["username"])
    return GitLabMessageV1(topic=topic, body={"body": body, "headers": headers, "agent": agent})
