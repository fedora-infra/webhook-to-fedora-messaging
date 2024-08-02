# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Use sqlalchemy-helpers.

Import the functions we will use in the main code and in migrations.
"""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_helpers import (  # noqa: F401
    Base,
    DatabaseManager,
    exists_in_db,
    get_or_create,
    is_sqlite,
    update_or_create,
)
from sqlalchemy_helpers.fastapi import make_db_session


db = None


async def setup_database():
    await db.sync()


async def get_session() -> AsyncIterator[AsyncSession]:
    async for session in make_db_session(db):
        yield session
