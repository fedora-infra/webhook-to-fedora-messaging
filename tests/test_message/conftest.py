from collections.abc import Generator
from unittest import mock

import pytest
from fedora_messaging.api import Message
from twisted.internet import defer
from twisted.internet.defer import Deferred

from webhook_to_fedora_messaging.fasjson import FASJSONAsyncProxy


@pytest.fixture()
def sent_messages() -> Generator[list[Message]]:
    """
    For confirming successful message dispatch
    """
    sent = []

    def _add_and_return(message: Message, exchange: str | None = None) -> Deferred[None]:
        sent.append(message)
        return defer.succeed(None)

    with mock.patch(
        "webhook_to_fedora_messaging.publishing.api.twisted_publish", side_effect=_add_and_return
    ):
        yield sent


@pytest.fixture()
def fasjson_client() -> Generator[FASJSONAsyncProxy, None]:
    """
    For resolving FAS usernames locally
    """
    client = FASJSONAsyncProxy("http://fasjson.example.com")
    parser_names = ("github", "forgejo", "gitlab", "pretix")
    patches = (
        mock.patch(
            f"webhook_to_fedora_messaging.endpoints.parser.{name}.get_fasjson",
            return_value=client,
        )
        for name in parser_names
    )
    with mock.patch.object(
        client, "search_users", mock.AsyncMock(return_value=[{"username": "dummy-fas-username"}])
    ):
        for patch in patches:
            patch.start()
        try:
            yield client
        finally:
            for patch in patches:
                patch.stop()
