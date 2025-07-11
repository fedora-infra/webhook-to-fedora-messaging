import hmac
import json
import pathlib
from collections.abc import Generator
from unittest import mock

import pytest
from fedora_messaging.api import Message
from fedora_messaging.exceptions import ConnectionException
from httpx import AsyncClient
from twisted.internet import defer
from twisted.internet.defer import Deferred
from webhook_to_fedora_messaging_messages.forgejo import ForgejoMessageV1
from webhook_to_fedora_messaging_messages.github import GitHubMessageV1
from webhook_to_fedora_messaging_messages.gitlab import GitLabMessageV1

from webhook_to_fedora_messaging.endpoints.parser.base import get_payload_sig
from webhook_to_fedora_messaging.fasjson import FASJSONAsyncProxy
from webhook_to_fedora_messaging.models.service import Service


@pytest.fixture()
def request_data(db_service: Service, event_type: str) -> str:
    fixtures_dir = pathlib.Path(__file__).parent.joinpath("fixtures").joinpath(db_service.type)
    try:
        with open(fixtures_dir.joinpath(f"{event_type}-payload.json")) as fh:
            return fh.read().strip()
    except OSError:
        pytest.skip(
            "Payload fixture for service type {db_service.type} and event type {event_type} not available"
        )


@pytest.fixture()
def request_headers(db_service: Service, event_type: str, request_data: str) -> dict[str, str]:
    fixtures_dir = pathlib.Path(__file__).parent.joinpath("fixtures").joinpath(db_service.type)
    try:
        with open(fixtures_dir.joinpath(f"{event_type}-headers.json")) as fh:
            headers_data = fh.read().strip()
    except OSError:
        pytest.skip(
            "Headers fixture for service type {db_service.type} and event type {event_type} not available"
        )
    headers: dict[str, str] = json.loads(headers_data)
    sign = get_payload_sig(request_data.encode("utf-8"), db_service.token, "sha256")
    headers["x-hub-signature-256"] = f"sha256={sign}"
    return headers


@pytest.fixture()
def expected_schema(service_type: str) -> type[Message]:
    if service_type == "github":
        return GitHubMessageV1
    elif service_type == "gitlab":
        return GitLabMessageV1
    elif service_type == "forgejo":
        return ForgejoMessageV1
    else:
        pytest.fail()


@pytest.fixture()
def expected_fas_username(service_type: str) -> str | None:
    if service_type == "github":
        return "dummy-fas-username"
    elif service_type == "gitlab":
        return "dummy-fas-username"
    elif service_type == "forgejo":
        return None
    else:
        pytest.fail()


@pytest.fixture()
def expected_topic(service_type: str, event_type: str) -> str:
    if service_type == "gitlab" and event_type == "pull_request":
        event_type = "merge_request"
    return f"{service_type}.{event_type}"


@pytest.fixture()
def fasjson_client() -> Generator[FASJSONAsyncProxy, None]:
    """
    For resolving FAS usernames locally
    """
    client = FASJSONAsyncProxy("http://fasjson.example.com")
    parser_names = ("github", "forgejo", "gitlab")
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


async def test_message_create(
    client: AsyncClient,
    service_type: str,
    event_type: str,
    db_service: Service,
    request_data: str,
    request_headers: dict[str, str],
    fasjson_client: FASJSONAsyncProxy,
    sent_messages: list[Message],
    expected_schema: type[Message],
    expected_fas_username: str | None,
    expected_topic: str,
) -> None:
    """
    Sending data and successfully creating message
    """
    response = await client.post(
        f"/api/v1/messages/{db_service.uuid}", content=request_data, headers=request_headers
    )
    assert response.status_code == 202, response.text
    assert len(sent_messages) == 1
    sent_msg = sent_messages[0]
    assert isinstance(sent_msg, expected_schema)
    assert sent_msg.topic == expected_topic
    assert sent_msg.agent_name == expected_fas_username
    assert sent_msg.body["body"] == json.loads(request_data)
    assert response.json() == {
        "data": {
            "message_id": sent_msg.id,
            "url": f"http://datagrepper.example.com/v2/id?id={sent_msg.id}&is_raw=true&size=extra-large",
        }
    }


async def test_message_create_failure(
    client: AsyncClient,
    db_service: Service,
    request_data: str,
    request_headers: dict[str, str],
    fasjson_client: FASJSONAsyncProxy,
) -> None:
    """
    Sending data but facing broken connection
    """
    with mock.patch(
        "webhook_to_fedora_messaging.publishing.api.twisted_publish",
        side_effect=ConnectionException,
    ):
        response = await client.post(
            f"/api/v1/messages/{db_service.uuid}", content=request_data, headers=request_headers
        )
    assert response.status_code == 502, response.text


async def test_message_create_400(
    client: AsyncClient,
    db_service: Service,
    request_data: str,
    request_headers: dict[str, str],
) -> None:
    """
    Sending data with wrong information
    """
    if db_service.type == "gitlab":
        pytest.skip("Gitlab does not sign webhooks")
    with mock.patch.object(hmac, "compare_digest", new=mock.MagicMock(return_value=False)):
        response = await client.post(
            f"/api/v1/messages/{db_service.uuid}", content=request_data, headers=request_headers
        )
    assert response.status_code == 400


async def test_message_create_404(client: AsyncClient) -> None:
    """
    Sending data to a non-existent service
    """
    response = await client.post("/api/v1/messages/non-existent", json={})
    assert response.status_code == 404


async def test_message_create_bad_request(client: AsyncClient, db_service: Service) -> None:
    """
    Sending data with wrong format
    """
    response = await client.post(f"/api/v1/messages/{db_service.uuid}", content="not json")
    assert response.status_code == 422


async def test_message_create_from_bot(
    client: AsyncClient,
    db_service: Service,
    request_data: str,
    request_headers: dict[str, str],
    fasjson_client: FASJSONAsyncProxy,
    sent_messages: list[Message],
) -> None:
    """
    Ignoring username lookups on bot actions
    """
    if db_service.type != "github":
        pytest.skip("Only Github bots are supported for now")
    request_data = request_data.replace('"login": "username",', '"login": "dummy[bot]",')
    request_sig = get_payload_sig(request_data.encode("utf-8"), db_service.token, "sha256")
    request_headers["x-hub-signature-256"] = f"sha256={request_sig}"
    response = await client.post(
        f"/api/v1/messages/{db_service.uuid}", content=request_data, headers=request_headers
    )
    assert response.status_code == 202, response.text
    fasjson_client.search_users.assert_not_awaited()  # type: ignore
    assert len(sent_messages) == 1
    sent_msg = sent_messages[0]
    assert sent_msg.agent_name is None
