import logging

from webhook_to_fedora_messaging.models.service import Service

from .github import github_parser


def parser(service: Service, headers: str):
    if service.type.lower() == "github":
        try:
            return github_parser(service.token, headers)
        except Exception:
            logging.exception("Message could not be parsed")
            raise
    else:
        raise ValueError(f"Unsupported service: {service.type}")
