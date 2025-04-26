from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Unicode,
)
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine


metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("username", Unicode, primary_key=True),
    Column("github_username", Unicode),
    Column("emails", Unicode),
    Column("full_name", String),
    Column("oauth_access_token", Unicode),
    Column("created_on", DateTime),
)

repos = Table(
    "repos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Unicode),
    Column("description", Unicode),
    Column("language", Unicode),
    Column("enabled", Boolean),
    Column("username", Unicode, ForeignKey("users.github_username")),
)

org_to_user = Table(
    "org_to_user_mapping",
    metadata,
    Column("org_id", Unicode, ForeignKey("users.github_username"), primary_key=True),
    Column("usr_id", Unicode, ForeignKey("users.github_username"), primary_key=True),
)


@asynccontextmanager
async def get_session(url: str) -> AsyncGenerator[AsyncConnection, None]:
    engine = create_async_engine(url)

    async with engine.begin() as conn:
        yield conn

    await engine.dispose()
