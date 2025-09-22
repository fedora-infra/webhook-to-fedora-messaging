from collections.abc import Generator
from unittest import mock

import pytest
from fedora_messaging.api import Message
from twisted.internet import defer
from twisted.internet.defer import Deferred


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
