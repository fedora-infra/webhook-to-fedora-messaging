# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Serving the JS UI through FastAPI.
"""

from typing import Any

from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from starlette.responses import Response
from starlette.types import Scope


class StaticFilesWithFallback(StaticFiles):

    def __init__(self, *args: Any, fallback: str, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.fallback = fallback

    async def get_response(self, path: str, scope: Scope) -> Response:
        try:
            return await super().get_response(path=path, scope=scope)
        except HTTPException as exc:
            if exc.status_code != 404:
                raise
            return await super().get_response(path=self.fallback, scope=scope)
