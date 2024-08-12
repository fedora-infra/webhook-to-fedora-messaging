# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
The values for any configuration variable that was not mentioned of in the
custom configuration file will be inherently taken from the default values
"""

import logging
from contextlib import asynccontextmanager

import uvicorn.config
from fastapi import FastAPI

from webhook_to_fedora_messaging.config import setup_config, setup_database_manager, standard
from webhook_to_fedora_messaging.endpoints import message, service, user


logger = logging.getLogger(__name__)

desc = "Webhook To Fedora Messaging"

tags_metadata = [
    {"name": "messages", "description": "Operations on messages"},
    {"name": "services", "description": "Operations on services"},
    {"name": "users", "description": "Operations on users"},
]

PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_config()
    setup_database_manager()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Webhook To Fedora Messaging",
        description=desc,
        contact={
            "name": "Fedora Infrastructure",
            "email": "infrastructure@lists.fedoraproject.org",
        },
        openapi_tags=tags_metadata,
        lifespan=lifespan,
    )

    app.include_router(user.router, prefix=PREFIX)
    app.include_router(service.router, prefix=PREFIX)
    app.include_router(message.router, prefix=PREFIX)

    return app


def start_service():
    loglevel_string = standard.main_logger_conf["handlers"]["console"]["level"]
    loglevel_number = uvicorn.config.LOG_LEVELS[loglevel_string.lower()]
    logger.info("Starting Webhook To Fedora Messaging...")
    logger.info(f"Host address     : {standard.service_host}")
    logger.info(f"Port number      : {standard.service_port}")
    logger.info(f"Log level        : {loglevel_string} / {loglevel_string}")
    logger.info(f"Reload on change : {str(standard.reload_on_change).upper()}")
    logger.info(f"Serving API docs on http://{standard.service_host}:{standard.service_port}/docs")
    uvicorn.run(
        "webhook_to_fedora_messaging.main:create_app",
        factory=True,
        host=standard.service_host,
        port=standard.service_port,
        log_level=loglevel_number,
        reload=standard.reload_on_change,
        log_config=standard.wsgi_logger_conf,
    )
