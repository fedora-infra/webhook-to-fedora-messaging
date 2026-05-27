from typing import Any

from webhook_to_fedora_messaging_messages.discourse import DiscourseMessageV1

from .base import BaseParser, Body, HeadersDict


class DiscourseParser(BaseParser):
    message_class = DiscourseMessageV1
    signature_header_name = "x-discourse-event-signature"

    def _get_topic(self, headers: HeadersDict, body: Body) -> str:
        return f"discourse.{headers['x-discourse-event-type']}.{headers['x-discourse-event']}"

    async def _get_message_body(
        self, body: dict[str, Any], headers: HeadersDict, agent: str | None
    ) -> dict[str, Any]:
        message_body: dict[str, Any] = {}
        # Filter the headers
        header_list = [
            "X-Discourse-Instance",
            "X-Discourse-Event-Id",
            "X-Discourse-Event-Type",
            "X-Discourse-Event",
            "X-Discourse-Event-Signature",
        ]
        message_body["webhook_headers"] = {
            headername: headers[headername.lower()] for headername in header_list
        }
        # Filter the body
        message_body["webhook_body"] = body
        # remove cooked and raw from the post in webhook body
        # (pagure.io/fedora-infrastructure/issue/10420)
        if "post" in message_body["webhook_body"]:
            message_body["webhook_body"]["post"].pop("cooked", None)
            message_body["webhook_body"]["post"].pop("raw", None)
        return message_body
