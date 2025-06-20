import hashlib
import hmac
import json
from typing import Any, TypeAlias

from fedora_messaging.api import Message
from starlette.requests import Request

from ...exceptions import SignatureMatchError


HeadersDict: TypeAlias = dict[str, str]
Body: TypeAlias = dict[str, Any]
BodyData: TypeAlias = bytes


class BaseParser:

    message_class: type[Message] = Message

    def __init__(self, token: str, request: Request):
        self._token = token
        self._request = request

    async def get_headers_and_data(self) -> tuple[HeadersDict, bytes]:
        headers = {k.lower(): v for k, v in self._request.headers.items()}
        if "x-hub-signature-256" not in headers:
            raise KeyError("Signature not found")
        data = await self._request.body()
        return headers, data

    async def validate(self, headers: HeadersDict, data: bytes) -> None:
        raise NotImplementedError

    def _get_topic(self, headers: HeadersDict, body: Body) -> str:
        raise NotImplementedError

    async def _get_agent(self, body: Body) -> str | None: ...

    def _validate_with_sig_header(self, sig_header: str, data: BodyData) -> None:
        """
        Verify the payload by validating its signature.
        """
        algorithm, signature = sig_header.split("=", 1)
        try:
            algo_function = getattr(hashlib, algorithm)
        except AttributeError as e:
            raise SignatureMatchError(f"Unsupported algorithm: {algorithm}") from e
        hash_object = hmac.new(self._token.encode("utf-8"), msg=data, digestmod=algo_function)
        if not hmac.compare_digest(hash_object.hexdigest(), signature):
            raise SignatureMatchError("Message signature could not be matched")

    async def parse(self) -> Message:
        headers, data = await self.get_headers_and_data()
        if self._token:
            await self.validate(headers, data)
        body = json.loads(data.decode("utf-8"))
        topic = self._get_topic(headers, body)
        agent = await self._get_agent(body)
        return self.message_class(
            topic=topic, body={"body": body, "headers": headers, "agent": agent}
        )
