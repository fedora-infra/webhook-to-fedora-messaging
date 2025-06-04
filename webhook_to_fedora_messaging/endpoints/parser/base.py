import json
from collections.abc import Awaitable
from functools import wraps
from typing import Any, Callable, TypeAlias

from fedora_messaging.api import Message
from starlette.requests import Request


HeadersDict: TypeAlias = dict[str, str]
Body: TypeAlias = dict[str, Any]
BodyData: TypeAlias = bytes


def initialize_parser(
    function: Callable[[str, HeadersDict, Body, BodyData], Awaitable[Message]],
) -> Callable[[str, Request], Awaitable[Message]]:
    @wraps(function)
    async def verify_before(token: str, request: Request) -> Message:
        headers = {k.lower(): v for k, v in request.headers.items()}
        if "x-hub-signature-256" not in headers:
            raise KeyError("Signature not found")
        data = await request.body()
        body = json.loads(data.decode("utf-8"))
        return await function(token, headers, body, data)

    return verify_before
