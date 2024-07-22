import pytest
import hmac
import json
import hashlib
import pathlib
from contextlib import nullcontext
from .event_sample import request, headers
from fedora_messaging.testing import mock_sends
from webhook_to_fedora_messaging_messages.github.github import GithubMessageV1


def signature_header(service, request):
    hashed_value = hmac.new(service.token.encode('utf-8'), msg=json.dumps(request, sort_keys=True).encode("utf-8"), digestmod=hashlib.sha256)
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


def test_message_create(client, create_service):
    headers = get_headers(create_service, request)
    with mock_sends(GithubMessageV1):
        response = client.post(f"/message/{create_service.uuid}", json=request, headers=headers)
    assert response.status_code == 200


@pytest.fixture
def request_data():
    fixtures_dir = pathlib.Path(__file__).parent.joinpath("fixtures")
    with open(fixtures_dir.joinpath("payload.json")) as fh:
        return fh.read().strip()


def test_message_create_400(client, create_service, request_data):
    headers = get_headers(create_service, request)
    headers["X-Hub-Signature-256"] = ""
    response = client.post(f"/message/{create_service.uuid}", data=request_data, headers=headers)
    assert response.status_code == 400


def test_message_create_404(client):
    response = client.post(f"/message/non-exsitent", json={})
    assert response.status_code == 404


def test_message_create_415(client, create_service):
    response = client.post(f"/message/{create_service.uuid}", data="not json")
    assert response.status_code == 415

