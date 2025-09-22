import json
from typing import Any

from fedora_messaging.api import Message
from webhook_to_fedora_messaging_messages.discourse import DiscourseMessageV1

from .base import BaseParser, Body, HeadersDict


class DiscourseParser(BaseParser):

    message_class = DiscourseMessageV1
    signature_header_name = "x-discourse-event-signature"

    def _get_topic(self, headers: HeadersDict, body: Body) -> str:
        return f"discourse.{headers['x-discourse-event-type']}.{headers['x-discourse-event']}"

    async def parse(self) -> Message:
        headers, data = await self.get_headers_and_data()
        await self.validate(headers, data)
        webhook_body = json.loads(data.decode("utf-8"))
        topic = self._get_topic(headers, webhook_body)
        body: dict[str, Any] = {}

        # Filter the headers
        header_list = [
            "X-Discourse-Instance",
            "X-Discourse-Event-Id",
            "X-Discourse-Event-Type",
            "X-Discourse-Event",
            "X-Discourse-Event-Signature",
        ]
        body["webhook_headers"] = {
            headername: headers[headername.lower()] for headername in header_list
        }
        # Filter the body
        body["webhook_body"] = webhook_body
        # remove cooked and raw from the post in webhook body
        # (pagure.io/fedora-infrastructure/issue/10420)
        if "post" in body["webhook_body"]:
            body["webhook_body"]["post"].pop("cooked", None)
            body["webhook_body"]["post"].pop("raw", None)

        return self.message_class(topic=topic, body=body)
