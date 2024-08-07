import hashlib
import hmac
import json
import pathlib
from types import SimpleNamespace
from unittest import mock

import pytest
from fedora_messaging.testing import mock_sends
from webhook_to_fedora_messaging_messages.github.github import GithubMessageV1


def signature_header(service, request):
    hashed_value = hmac.new(
        service.token.encode("utf-8"),
        msg=request.encode("utf-8"),
        digestmod=hashlib.sha256,
    )
    return hashed_value.hexdigest()


def get_headers(service, request):
    return {
        "Content-Type": "application/json",
        "X-Hub-Signature-256": f"sha256={signature_header(service, request)}",
        "X-Github-Event": "push",
        "X-Github-Delivery": "f1064eb2-4995-11ef-82e4-18ae0022c13c",
        "X-Github-Hook-Id": "491622597",
        "X-Github-Hook-Installation-Target-Id": "807808293",
        "X-Github-Hook-Installation-Target-Type": "repository",
        "X-Hub-Signature": "sha1=0e44dae9a9c979dc05d1f5846b06fe578e581533",
    }


@pytest.fixture
def request_data():
    fixtures_dir = pathlib.Path(__file__).parent.joinpath("fixtures")
    with open(fixtures_dir.joinpath("payload.json")) as fh:
        return fh.read().strip()


@pytest.fixture()
def fasjson_client():
    client = mock.Mock(name="fasjson")
    with mock.patch(
        "webhook_to_fedora_messaging.endpoints.parser.github.fasjson_client.Client",
        return_value=client,
    ):
        yield client


def test_message_create(client, db_service, request_data, fasjson_client):
    fasjson_client.search.return_value = SimpleNamespace(
        result=[{"username": "dummy-fas-username"}]
    )
    headers = get_headers(db_service, request_data)
    with mock_sends(GithubMessageV1) as sent_msgs:
        response = client.post(f"/message/{db_service.uuid}", data=request_data, headers=headers)
        print(response.data)
        assert response.status_code == 200
    sent_msg = sent_msgs[0]
    assert response.json["message_id"] == sent_msg.id
    assert sent_msg.topic == "github.push"
    assert sent_msg.agent_name == "dummy-fas-username"
    assert sent_msg.body["body"] == json.loads(request_data)


def test_message_create_400(client, db_service, request_data):
    headers = get_headers(db_service, request_data)
    headers["X-Hub-Signature-256"] = ""
    response = client.post(f"/message/{db_service.uuid}", data=request_data, headers=headers)
    assert response.status_code == 400


def test_message_create_404(client):
    response = client.post("/message/non-exsitent", json={})
    assert response.status_code == 404


def test_message_create_415(client, db_service):
    response = client.post(f"/message/{db_service.uuid}", data="not json")
    assert response.status_code == 415
