import logging

from webhook_to_fedora_messaging.models.service import Service

from .github import github_parser


logger = logging.getLogger(__name__)


def parser(service: Service, headers: str, body: dict):
    if service.type.lower() == "github":
        try:
            return github_parser(service.token, headers, body)
        except Exception:
            logger.exception("Message could not be parsed")
            raise
    else:
        raise ValueError(f"Unsupported service: {service.type}")
