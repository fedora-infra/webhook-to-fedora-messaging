# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Use sqlalchemy-helpers.

Import the functions we will use in the main code and in migrations.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from functools import cache

from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
from sqlalchemy_helpers.aio import (  # noqa: F401
    AsyncDatabaseManager,
    get_or_create,
    update_or_create,
)
from sqlalchemy_helpers.fastapi import make_db_session, manager_from_config
from sqlalchemy_helpers.manager import get_base

from .config import get_config


# Add https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
Base = get_base(cls=AsyncAttrs)


@cache
def get_db_manager() -> AsyncDatabaseManager:
    config = get_config()
    return manager_from_config(config.database, base_model=Base)


async def setup_database():
    db = get_db_manager()
    # Populate Base.metadata
    from . import models  # noqa: F401

    return await db.sync()


async def get_session() -> AsyncIterator[AsyncSession]:
    db = get_db_manager()
    async for session in make_db_session(db):
        yield session


with_db_session = asynccontextmanager(get_session)
