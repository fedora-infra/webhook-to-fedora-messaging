# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Use sqlalchemy-helpers.

Import the functions we will use in the main code and in migrations.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from functools import cache

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_helpers.aio import (
    AsyncDatabaseManager,
    Base,
    get_or_create,
    update_or_create,
)
from sqlalchemy_helpers.fastapi import make_db_session, manager_from_config
from sqlalchemy_helpers.manager import SyncResult

from .config import get_config


__all__ = (
    "Base",
    "get_db_manager",
    "get_or_create",
    "get_session",
    "setup_database",
    "update_or_create",
    "with_db_session",
)


@cache
def get_db_manager() -> AsyncDatabaseManager:
    config = get_config()
    return manager_from_config(config.database, base_model=Base)


async def setup_database() -> SyncResult:
    db = get_db_manager()
    # Populate Base.metadata
    from . import models  # noqa: F401

    return await db.sync()


async def get_session() -> AsyncGenerator[AsyncSession]:
    db = get_db_manager()
    async for session in make_db_session(db):
        yield session


with_db_session = asynccontextmanager(get_session)
