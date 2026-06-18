import json
from collections.abc import AsyncGenerator
from typing import Any

import httpx
import pytest
import respx
from fedora_messaging.api import Message
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from webhook_to_fedora_messaging_messages.pretix import PretixMessageV1

from webhook_to_fedora_messaging.fasjson import FASJSONAsyncProxy
from webhook_to_fedora_messaging.models.service import Service
from webhook_to_fedora_messaging.models.user import User

from ..utils import make_db_service


@pytest.fixture()
async def db_service(
    db_user: User,
    db_session: AsyncSession,
) -> AsyncGenerator[Service]:
    service = await make_db_service(db_session, "pretix", db_user)
    yield service
    # Teardown code to remove the object from the database
    await db_session.delete(service)
    await db_session.commit()


@pytest.fixture()
def base_data() -> dict[str, Any]:
    return {
        "notification_id": 10514,
        "organizer": "community",
        "event": "flock-2026",
    }


@pytest.fixture()
def base_checkin_data(base_data: dict[str, Any]) -> dict[str, Any]:
    data = base_data
    data.update(
        {
            "action": "pretix.event.checkin",
            "code": "YTSDG",
            "type": "entry",
            "orderposition_id": 905,
            "orderposition_positionid": 1,
            "checkin_list": 15,
            "first_checkin": None,
        }
    )
    return data


async def test_pretix_checkin(
    client: AsyncClient,
    db_service: Service,
    sent_messages: list[Message],
    base_checkin_data: dict[str, Any],
    fasjson_client: FASJSONAsyncProxy,
    respx_mock: respx.MockRouter,
) -> None:
    data = base_checkin_data
    event = {
        "positions": [
            {
                "attendee_name": "Dummy User",
                "attendee_email": "dummy@example.com",
            }
        ]
    }
    respx_mock.get(
        "http://pretix.example.com/api/v1/organizers/community/events/flock-2026/orders/YTSDG/"
    ).mock(httpx.Response(200, json=event))
    response = await client.post(
        f"/api/v1/messages/{db_service.uuid}",
        content=json.dumps(data),
        headers={
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 202, response.text
    assert len(sent_messages) == 1
    sent_msg = sent_messages[0]
    assert isinstance(sent_msg, PretixMessageV1)
    assert sent_msg.topic == "pretix.event.checkin"
    assert sent_msg.agent_name == "dummy-fas-username"
    expected_data = {"attendee_name": "Dummy User", "instance_url": "http://pretix.example.com"}
    expected_data.update(data)
    assert sent_msg.body["body"] == expected_data
    assert response.json() == {"data": {"message_id": None, "url": None}}
    fasjson_client.search_users.assert_awaited_once()  # type: ignore


async def test_pretix_not_checkin(
    client: AsyncClient,
    db_service: Service,
    base_data: dict[str, Any],
    sent_messages: list[Message],
    fasjson_client: FASJSONAsyncProxy,
) -> None:
    data = base_data
    data["action"] = "pretix.dummy"
    response = await client.post(
        f"/api/v1/messages/{db_service.uuid}",
        content=json.dumps(data),
        headers={
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 202, response.text
    assert len(sent_messages) == 1
    sent_msg = sent_messages[0]
    assert isinstance(sent_msg, PretixMessageV1)
    assert sent_msg.topic == "pretix.dummy"
    assert sent_msg.agent_name is None
    expected_data = {"attendee_name": None, "instance_url": "http://pretix.example.com"}
    expected_data.update(data)
    assert sent_msg.body["body"] == expected_data
    fasjson_client.search_users.assert_not_awaited()  # type: ignore
    assert response.json() == {"data": {"message_id": None, "url": None}}


async def test_pretix_no_event(
    client: AsyncClient,
    db_service: Service,
    base_checkin_data: dict[str, Any],
    sent_messages: list[Message],
    fasjson_client: FASJSONAsyncProxy,
) -> None:
    data = base_checkin_data
    del data["event"]
    response = await client.post(
        f"/api/v1/messages/{db_service.uuid}",
        content=json.dumps(data),
        headers={
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 202, response.text
    assert len(sent_messages) == 1
    sent_msg = sent_messages[0]
    assert isinstance(sent_msg, PretixMessageV1)
    assert sent_msg.agent_name is None
    expected_data = {"attendee_name": None, "instance_url": "http://pretix.example.com"}
    expected_data.update(data)
    assert sent_msg.body["body"] == expected_data
    fasjson_client.search_users.assert_not_awaited()  # type: ignore


async def test_pretix_checkin_bad_api(
    client: AsyncClient,
    db_service: Service,
    sent_messages: list[Message],
    base_checkin_data: dict[str, Any],
    fasjson_client: FASJSONAsyncProxy,
    respx_mock: respx.MockRouter,
) -> None:
    data = base_checkin_data
    respx_mock.get(
        "http://pretix.example.com/api/v1/organizers/community/events/flock-2026/orders/YTSDG/"
    ).mock(httpx.Response(500, json={"error": "dummy"}))
    response = await client.post(
        f"/api/v1/messages/{db_service.uuid}",
        content=json.dumps(data),
        headers={
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 202, response.text
    assert len(sent_messages) == 1
    sent_msg = sent_messages[0]
    assert isinstance(sent_msg, PretixMessageV1)
    assert sent_msg.topic == "pretix.event.checkin"
    assert sent_msg.agent_name is None
    expected_data = {"attendee_name": None, "instance_url": "http://pretix.example.com"}
    expected_data.update(data)
    assert sent_msg.body["body"] == expected_data
    fasjson_client.search_users.assert_not_awaited()  # type: ignore


async def test_pretix_checkin_wrong_api_response(
    client: AsyncClient,
    db_service: Service,
    sent_messages: list[Message],
    base_checkin_data: dict[str, Any],
    fasjson_client: FASJSONAsyncProxy,
    respx_mock: respx.MockRouter,
) -> None:
    data = base_checkin_data
    event: dict[str, Any] = {"positions": []}
    respx_mock.get(
        "http://pretix.example.com/api/v1/organizers/community/events/flock-2026/orders/YTSDG/"
    ).mock(httpx.Response(200, json=event))
    response = await client.post(
        f"/api/v1/messages/{db_service.uuid}",
        content=json.dumps(data),
        headers={
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 202, response.text
    assert len(sent_messages) == 1
    sent_msg = sent_messages[0]
    assert isinstance(sent_msg, PretixMessageV1)
    assert sent_msg.topic == "pretix.event.checkin"
    assert sent_msg.agent_name is None
    expected_data = {"attendee_name": None, "instance_url": "http://pretix.example.com"}
    expected_data.update(data)
    assert sent_msg.body["body"] == expected_data
    assert response.json() == {"data": {"message_id": None, "url": None}}
    fasjson_client.search_users.assert_not_awaited()  # type: ignore


async def test_pretix_checkin_fpo_email(
    client: AsyncClient,
    db_service: Service,
    sent_messages: list[Message],
    base_checkin_data: dict[str, Any],
    fasjson_client: FASJSONAsyncProxy,
    respx_mock: respx.MockRouter,
) -> None:
    data = base_checkin_data
    event = {
        "positions": [
            {
                "attendee_name": "Dummy User",
                "attendee_email": "fasuser@fedoraproject.org",
            }
        ]
    }
    respx_mock.get(
        "http://pretix.example.com/api/v1/organizers/community/events/flock-2026/orders/YTSDG/"
    ).mock(httpx.Response(200, json=event))
    response = await client.post(
        f"/api/v1/messages/{db_service.uuid}",
        content=json.dumps(data),
        headers={
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 202, response.text
    assert len(sent_messages) == 1
    sent_msg = sent_messages[0]
    assert isinstance(sent_msg, PretixMessageV1)
    assert sent_msg.agent_name == "fasuser"
    fasjson_client.search_users.assert_not_awaited()  # type: ignore
