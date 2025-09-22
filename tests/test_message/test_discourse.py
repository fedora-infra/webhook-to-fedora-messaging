import json
from collections.abc import AsyncGenerator
from typing import Any

import pytest
from fedora_messaging.api import Message
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from webhook_to_fedora_messaging_messages.discourse import DiscourseMessageV1

from webhook_to_fedora_messaging.endpoints.parser.base import get_payload_sig
from webhook_to_fedora_messaging.models.service import Service
from webhook_to_fedora_messaging.models.user import User

from ..utils import make_db_service


@pytest.fixture()
async def db_service(
    db_user: User,
    db_session: AsyncSession,
) -> AsyncGenerator[Service]:
    service = await make_db_service(db_session, "discourse", db_user)
    yield service
    # Teardown code to remove the object from the database
    await db_session.delete(service)
    await db_session.commit()


def calc_sig(db_service: Service, data: dict[str, Any]) -> str:
    return get_payload_sig(json.dumps(data).encode(), db_service.token, "sha256")


async def test_discourse_ping(
    client: AsyncClient,
    db_service: Service,
    sent_messages: list[Message],
) -> None:
    data = {"ping": "OK"}
    headers = {
        "X-Discourse-Event-Signature": f"sha256={calc_sig(db_service, data)}",
        "X-Discourse-Event-Type": "ping",
        "X-Discourse-Event": "ping",
        "X-Discourse-Instance": "discourse.test",
        "X-Discourse-Event-Id": "1",
    }

    response = await client.post(
        f"/api/v1/messages/{db_service.uuid}", content=json.dumps(data), headers=headers
    )

    assert response.status_code == 202, response.text
    assert len(sent_messages) == 1
    sent_msg = sent_messages[0]
    assert isinstance(sent_msg, DiscourseMessageV1)
    assert sent_msg.topic == "discourse.ping.ping"
    assert sent_msg.agent_name is None
    assert sent_msg.body["webhook_body"] == data
    assert sent_msg.body["webhook_headers"] == headers
    assert response.json() == {
        "data": {
            "message_id": sent_msg.id,
            "url": f"http://datagrepper.example.com/v2/id?id={sent_msg.id}&is_raw=true&size=extra-large",
        }
    }


async def test_discourse_remove_cooked_raw(
    client: AsyncClient,
    db_service: Service,
    sent_messages: list[Message],
) -> None:
    data = {"ping": "OK", "post": {"cooked": "yummy", "raw": "eeew", "post_number": 11}}
    headers = {
        "X-Discourse-Event-Signature": f"sha256={calc_sig(db_service, data)}",
        "X-Discourse-Event-Type": "ping",
        "X-Discourse-Event": "ping",
        "X-Discourse-Instance": "discourse.test",
        "X-Discourse-Event-Id": "1",
    }
    response = await client.post(
        f"/api/v1/messages/{db_service.uuid}", content=json.dumps(data), headers=headers
    )

    assert response.status_code == 202, response.text
    assert len(sent_messages) == 1
    sent_msg = sent_messages[0]
    # The body here should not have cooked or raw keys...
    assert sent_msg.body["webhook_body"] == {"ping": "OK", "post": {"post_number": 11}}
    assert sent_msg.body["webhook_headers"] == headers
    assert response.json() == {
        "data": {
            "message_id": sent_msg.id,
            "url": f"http://datagrepper.example.com/v2/id?id={sent_msg.id}&is_raw=true&size=extra-large",
        }
    }


async def test_discourse_missing_header(
    client: AsyncClient,
    db_service: Service,
    sent_messages: list[Message],
) -> None:
    data = {"test_data": "data"}
    response = await client.post(f"/api/v1/messages/{db_service.uuid}", content=json.dumps(data))

    assert response.status_code == 400, response.text
    assert len(sent_messages) == 0
    assert response.json() == {"detail": "Message could not be dispatched - 'Signature not found'"}


async def test_discourse_wrong_hash(
    client: AsyncClient,
    db_service: Service,
    sent_messages: list[Message],
) -> None:
    data = {"test_data": "data"}
    response = await client.post(
        f"/api/v1/messages/{db_service.uuid}",
        content=json.dumps(data),
        headers={
            "X-Discourse-Event-Signature": calc_sig(db_service, data),
            "X-Discourse-Event-Type": "test_event",
        },
    )

    assert response.status_code == 400, response.text
    assert len(sent_messages) == 0
    assert response.json() == {
        "detail": "Message could not be dispatched - not enough values to unpack (expected 2, got 1)"
    }


async def test_discourse_not_valid_sig(
    client: AsyncClient,
    db_service: Service,
    sent_messages: list[Message],
) -> None:
    data = {"test_data": "data"}
    response = await client.post(
        f"/api/v1/messages/{db_service.uuid}",
        content=json.dumps(data),
        headers={
            "X-Discourse-Event-Signature": "sha256=dummy",
            "X-Discourse-Event-Type": "test_event",
        },
    )

    assert response.status_code == 400, response.text
    assert len(sent_messages) == 0
    assert response.json() == {
        "detail": "Message could not be dispatched - Message signature could not be matched"
    }
