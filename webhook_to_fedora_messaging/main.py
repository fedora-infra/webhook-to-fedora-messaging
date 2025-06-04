# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
The values for any configuration variable that was not mentioned of in the
custom configuration file will be inherently taken from the default values
"""

import importlib.metadata
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

from .cache import configure_cache
from .config import get_config
from .database import get_db_manager
from .endpoints import message, service, user
from .fasjson import get_fasjson


logger = logging.getLogger(__name__)

desc = "Webhook To Fedora Messaging"

tags_metadata = [
    {"name": "messages", "description": "Operations on messages"},
    {"name": "services", "description": "Operations on services"},
    {"name": "users", "description": "Operations on users"},
]

PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    # Initialize long-lived objects
    get_db_manager()
    configure_cache()
    get_fasjson()
    yield


def create_app() -> FastAPI:
    config = get_config()
    app = FastAPI(
        title="Webhook To Fedora Messaging",
        description=desc,
        contact={
            "name": "Fedora Infrastructure",
            "email": "infrastructure@lists.fedoraproject.org",
        },
        version=importlib.metadata.version("webhook-to-fedora-messaging"),
        openapi_tags=tags_metadata,
        swagger_ui_init_oauth={
            "clientId": config.oidc.client_id,
            "clientSecret": "",
            "scopes": config.oidc.scopes,
        },
        lifespan=lifespan,
    )

    # We need this for auth to save temporary code & state in session.
    # We don't need an actual secret key, a random one is fine, since the auth data is only there
    # during the auth process.
    app.add_middleware(SessionMiddleware, secret_key=config.session_secret)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routes
    app.include_router(user.router, prefix=PREFIX)
    app.include_router(service.router, prefix=PREFIX)
    app.include_router(message.router, prefix=PREFIX)

    async def _redirect_to_docs(request: Request) -> RedirectResponse:
        return RedirectResponse(app.docs_url or "/docs")

    app.add_route("/", _redirect_to_docs, include_in_schema=False)

    return app
