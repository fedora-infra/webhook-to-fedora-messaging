import hmac
import json
import pathlib
from collections.abc import Generator
from unittest import mock

import pytest
from fedora_messaging.api import Message
from fedora_messaging.exceptions import ConnectionException
from httpx import AsyncClient
from pytest import FixtureRequest
from twisted.internet import defer
from twisted.internet.defer import Deferred
from webhook_to_fedora_messaging_messages.forgejo import ForgejoMessageV1
from webhook_to_fedora_messaging_messages.github import GitHubMessageV1

from webhook_to_fedora_messaging.endpoints.parser.base import get_payload_sig
from webhook_to_fedora_messaging.fasjson import FASJSONAsyncProxy
from webhook_to_fedora_messaging.models.service import Service


@pytest.fixture()
def request_data(request: FixtureRequest) -> str:
    """
    For setting the correct body information
    """
    fixtures_dir = pathlib.Path(__file__).parent.joinpath("fixtures")
    with open(fixtures_dir.joinpath(f"payload_{request.param}.json")) as fh:
        return fh.read().strip()


@pytest.fixture()
def request_headers(
    request: FixtureRequest, db_service: Service, request_data: str
) -> dict[str, str]:
    """
    For setting the correct header information
    """
    fixtures_dir = pathlib.Path(__file__).parent.joinpath("fixtures")
    with open(fixtures_dir.joinpath(f"headers_{request.param}.json")) as fh:
        data = fh.read().strip()
    headers: dict[str, str] = json.loads(data)
    sign = get_payload_sig(request_data.encode("utf-8"), db_service.token, "sha256")
    headers["x-hub-signature-256"] = f"sha256={sign}"
    return headers


@pytest.fixture()
def fasjson_client() -> Generator[mock.Mock, None]:
    """
    For resolving FAS usernames locally
    """
    client = mock.Mock(name="fasjson")
    with mock.patch(
        "webhook_to_fedora_messaging.endpoints.parser.github.get_fasjson",
        return_value=client,
    ):
        yield client


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


@pytest.mark.parametrize(
    "kind, schema, username, request_data, db_service, request_headers",
    [
        pytest.param(
            "github",
            GitHubMessageV1,
            "dummy-fas-username",
            "github",
            "github",
            "github",
            id="GitHub",
        ),
        pytest.param(
            "forgejo",
            ForgejoMessageV1,
            "gridhead",
            "forgejo",
            "forgejo",
            "forgejo",
            id="Forgejo",
        ),
    ],
    indirect=["request_data", "db_service", "request_headers"],
)
async def test_message_create(
    client: AsyncClient,
    db_service: Service,
    request_data: str,
    request_headers: dict[str, str],
    fasjson_client: mock.Mock,
    sent_messages: list[Message],
    kind: str,
    schema: type[Message],
    username: str,
) -> None:
    """
    Sending data and successfully creating message
    """
    setattr(
        fasjson_client,
        f"get_username_from_{kind}",
        mock.AsyncMock(return_value="dummy-fas-username"),
    )
    response = await client.post(
        f"/api/v1/messages/{db_service.uuid}", content=request_data, headers=request_headers
    )
    assert response.status_code == 202, response.text
    assert len(sent_messages) == 1
    sent_msg = sent_messages[0]
    assert isinstance(sent_msg, schema)
    assert sent_msg.topic == f"{kind}.push"
    if kind == "github":
        assert sent_msg.agent_name == username
    else:
        # FAJSON only has mapping data for Github at the moment
        assert sent_msg.agent_name is None
    assert sent_msg.body["body"] == json.loads(request_data)
    assert response.json() == {
        "data": {
            "message_id": sent_msg.id,
            "url": f"http://datagrepper.example.com/v2/id?id={sent_msg.id}&is_raw=true&size=extra-large",
        }
    }


@pytest.mark.parametrize(
    "kind, username, request_data, db_service, request_headers",
    [
        pytest.param(
            "github",
            "dummy-fas-username",
            "github",
            "github",
            "github",
            id="GitHub",
        ),
        pytest.param(
            "forgejo",
            "gridhgead",
            "forgejo",
            "forgejo",
            "forgejo",
            id="Forgejo",
        ),
    ],
    indirect=["request_data", "db_service", "request_headers"],
)
async def test_message_create_failure(
    client: AsyncClient,
    db_service: Service,
    request_data: str,
    request_headers: dict[str, str],
    fasjson_client: mock.Mock,
    kind: str,
    username: str,
) -> None:
    """
    Sending data but facing broken connection
    """
    setattr(
        fasjson_client,
        f"get_username_from_{kind}",
        mock.AsyncMock(return_value=username),
    )
    with mock.patch(
        "webhook_to_fedora_messaging.publishing.api.twisted_publish",
        side_effect=ConnectionException,
    ):
        response = await client.post(
            f"/api/v1/messages/{db_service.uuid}", content=request_data, headers=request_headers
        )
    assert response.status_code == 502, response.text


@pytest.mark.parametrize(
    "kind, request_data, db_service, request_headers",
    [
        pytest.param(
            "github",
            "github",
            "github",
            "github",
            id="GitHub",
        ),
        pytest.param(
            "forgejo",
            "forgejo",
            "forgejo",
            "forgejo",
            id="Forgejo",
        ),
    ],
    indirect=["request_data", "db_service", "request_headers"],
)
async def test_message_create_400(
    client: AsyncClient,
    db_service: Service,
    request_data: str,
    request_headers: dict[str, str],
    kind: str,
) -> None:
    """
    Sending data with wrong information
    """
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


@pytest.mark.parametrize(
    "db_service",
    [
        pytest.param(
            "github",
            id="GitHub",
        ),
        pytest.param(
            "forgejo",
            id="Forgejo",
        ),
    ],
    indirect=["db_service"],
)
async def test_message_create_bad_request(client: AsyncClient, db_service: Service) -> None:
    """
    Sending data with wrong format
    """
    response = await client.post(f"/api/v1/messages/{db_service.uuid}", content="not json")
    assert response.status_code == 422


@pytest.mark.parametrize(
    "kind, username, request_data, db_service, request_headers",
    [
        pytest.param(
            "github",
            "dummy[bot]",
            "github",
            "github",
            "github",
            id="GitHub",
        ),
    ],
    indirect=["request_data", "db_service", "request_headers"],
)
async def test_message_create_from_bot(
    client: AsyncClient,
    db_service: Service,
    request_data: str,
    request_headers: dict[str, str],
    sent_messages: list[Message],
    kind: str,
    username: str,
) -> None:
    """
    Ignoring username lookups on bot actions
    """
    request_data = request_data.replace('"login": "username",', f'"login": "{username}",')
    request_sig = get_payload_sig(request_data.encode("utf-8"), db_service.token, "sha256")
    request_headers["x-hub-signature-256"] = f"sha256={request_sig}"
    fasjson_client = FASJSONAsyncProxy("http://fasjson.example.com")
    with mock.patch(
        "webhook_to_fedora_messaging.endpoints.parser.github.get_fasjson",
        return_value=fasjson_client,
    ), mock.patch.object(
        fasjson_client,
        "search_users",
        new=mock.AsyncMock(return_value=[{"username": "dummy-fas-username"}]),
    ):
        response = await client.post(
            f"/api/v1/messages/{db_service.uuid}", content=request_data, headers=request_headers
        )
        assert response.status_code == 202, response.text
        fasjson_client.search_users.assert_not_awaited()  # type: ignore
    assert len(sent_messages) == 1
    sent_msg = sent_messages[0]
    assert sent_msg.agent_name is None
