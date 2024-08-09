import hashlib
import hmac
import json

import fasjson_client
from starlette.datastructures import Headers
from webhook_to_fedora_messaging_messages.github.github import GithubMessageV1

from webhook_to_fedora_messaging.config import standard
from webhook_to_fedora_messaging.exceptions import SignatureMatchError


def github_parser(token: str, headers: Headers, body: dict) -> GithubMessageV1:
    """Convert Flask request objects into desired FedMsg format.

    Args:
        token: Specifies whether the webhook has token key feature on or not
    """

    headers = dict(headers)

    if "X-Hub-Signature-256" not in headers:
        raise KeyError("Signature not found")

    if token and not verify_signature(token, headers["X-Hub-Signature-256"], body):
        raise SignatureMatchError("Message Signature Couldn't be Matched.")

    topic = f"github.{headers['X-Github-Event']}"
    agent = fas_by_github(body["sender"]["login"])  # FASJSON
    return GithubMessageV1(
        topic=topic, body={"body": body, "headers": headers, "agent": agent}
    )


def verify_signature(token: str, signature_header: str, body: dict) -> bool:
    """Verify that the payload was sent from GitHub by validating SHA256.

    Return false if not authorized.

    Args:
        token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    if not signature_header:
        return False
    hash_object = hmac.new(
        token.encode("utf-8"),
        msg=json.dumps(body).encode(),
        digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()

    return hmac.compare_digest(expected_signature, signature_header)


def fas_by_github(username: str) -> str:
    """Get the Fedora Account System Username of the given GitHub username

    Args:
        username: GitHub Username"""

    fasjson = fasjson_client.Client(standard.fasjson_url)
    response = fasjson.search(github_username=username)
    if response.result and len(response.result) == 1:
        return response.result[0]["username"]
    return None
