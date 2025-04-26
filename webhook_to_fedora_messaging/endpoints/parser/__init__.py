import logging

from starlette.requests import Request
from webhook_to_fedora_messaging_messages.forgejo import ForgejoMessageV1
from webhook_to_fedora_messaging_messages.github import GitHubMessageV1

from ..service import Service
from .forgejo import forgejo_parser
from .github import github_parser


logger = logging.getLogger(__name__)


async def parser(service: Service, request: Request) -> ForgejoMessageV1 | GitHubMessageV1:
    parsers = {
        "github": github_parser,
        "forgejo": forgejo_parser,
    }

    parser_func = parsers.get(service.type.lower())
    if not parser_func:
        raise ValueError(f"Unsupported service: {service.type}")

    try:
        return await parser_func(service.token, request)
    except Exception:
        logger.exception("Message could not be parsed")
        raise
