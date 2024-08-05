import hashlib
import hmac

import fasjson_client
from flask import current_app, request
from starlette.datastructures import Headers
from webhook_to_fedora_messaging_messages.github.github import GithubMessageV1

from webhook_to_fedora_messaging.exceptions import SignatureMatchError


def github_parser(token: str, headers: Headers) -> GithubMessageV1:
    """Convert Flask request objects into desired FedMsg format.

    Args:
        token: Specifies whether the webhook has token key feature on or not
    """

    headers = dict(headers)

    if "X-Hub-Signature-256" not in headers:
        raise KeyError("Signature not found")

    if token and not verify_signature(token, headers["X-Hub-Signature-256"]):
        raise SignatureMatchError("Message Signature Couldn't be Matched.")

    topic = f"github.{headers['X-Github-Event']}"
    agent = fas_by_github(request.json["sender"]["login"])  # FASJSON
    return GithubMessageV1(
        topic=topic, body={"body": request.json, "headers": headers, "agent": agent}
    )


def verify_signature(token: str, signature_header: str) -> bool:
    """Verify that the payload was sent from GitHub by validating SHA256.

    Return false if not authorized.

    Args:
        token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    if not signature_header:
        return False
    hash_object = hmac.new(token.encode("utf-8"), msg=request.data, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()

    return hmac.compare_digest(expected_signature, signature_header)


def fas_by_github(username: str) -> str:
    """Get the Fedora Account System Username of the given GitHub username

    Args:
        username: GitHub Username"""

    fasjson = fasjson_client.Client(current_app.config["FASJSON_URL"])
    response = fasjson.search(github_username=username)
    if response.result and len(response.result) == 1:
        return response.result[0]["username"]
    return None
