import logging

from starlette.requests import Request

from webhook_to_fedora_messaging.models.service import Service

from .github import github_parser


logger = logging.getLogger(__name__)


async def parser(service: Service, request: Request):
    if service.type.lower() == "github":
        try:
            return await github_parser(service.token, request)
        except Exception:
            logger.exception("Message could not be parsed")
            raise
    else:
        raise ValueError(f"Unsupported service: {service.type}")
