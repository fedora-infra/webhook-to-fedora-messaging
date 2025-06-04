import hmac
from collections.abc import Awaitable
from functools import wraps
from hashlib import sha256
from typing import Callable

from fedora_messaging.api import Message
from webhook_to_fedora_messaging_messages.github import GitHubMessageV1

from ...endpoints.parser.base import initialize_parser
from ...exceptions import SignatureMatchError
from ...fasjson import get_fasjson
from .base import Body, BodyData, HeadersDict


def validate_checksum(
    function: Callable[[HeadersDict, Body], Awaitable[Message]],
) -> Callable[[str, HeadersDict, Body, BodyData], Awaitable[Message]]:
    @wraps(function)
    async def verify_before(
        token: str, headers: HeadersDict, body: Body, data: BodyData
    ) -> Message:
        """
        Verify that the payload was sent from GitHub by validating SHA256.
        """
        if token:
            sign = headers["x-hub-signature-256"]
            hash_object = hmac.new(token.encode("utf-8"), msg=data, digestmod=sha256)
            expected = f"sha256={hash_object.hexdigest()}"
            if not hmac.compare_digest(expected, sign):
                raise SignatureMatchError("Message signature could not be matched")
        return await function(headers, body)

    return verify_before


@initialize_parser
@validate_checksum
async def github_parser(headers: HeadersDict, body: Body) -> GitHubMessageV1:
    """
    Convert request objects into desired Fedora Messaging format
    """
    topic = f"github.{headers['x-github-event']}"
    agent = await get_fasjson().get_username_from_github(body["sender"]["login"])
    return GitHubMessageV1(topic=topic, body={"body": body, "headers": headers, "agent": agent})
