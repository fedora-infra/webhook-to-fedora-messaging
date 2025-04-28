import json
from functools import wraps
from typing import Callable

from starlette.requests import Request


def initialize_parser(function: Callable) -> Callable:
    @wraps(function)
    async def verify_before(token: str, request: Request) -> Callable:
        headers = {k.lower(): v for k, v in request.headers.items()}
        if "x-hub-signature-256" not in headers:
            raise KeyError("Signature not found")
        data = await request.body()
        body = json.loads(data.decode("utf-8"))
        return await function(token, headers, body, data)

    return verify_before
