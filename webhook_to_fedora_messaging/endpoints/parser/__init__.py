import logging

from fedora_messaging.api import Message
from starlette.requests import Request

from ...models import Service
from .forgejo import ForgejoParser
from .github import GitHubParser


logger = logging.getLogger(__name__)


async def parser(service: Service, request: Request) -> Message:
    parsers = {
        "github": GitHubParser,
        "forgejo": ForgejoParser,
    }

    parser = parsers.get(service.type.lower())
    if not parser:
        raise ValueError(f"Unsupported service: {service.type}")

    try:
        return await parser(service.token, request).parse()
    except Exception:
        logger.exception("Message could not be parsed")
        raise
