# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import AsyncGenerator
from pathlib import PosixPath
from unittest import mock

import pytest
from httpx import ASGITransport, AsyncClient, Headers
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_helpers.aio import AsyncDatabaseManager

from webhook_to_fedora_messaging import database
from webhook_to_fedora_messaging.config import set_config_file
from webhook_to_fedora_messaging.database import get_db_manager
from webhook_to_fedora_messaging.main import create_app
from webhook_to_fedora_messaging.models.service import Service
from webhook_to_fedora_messaging.models.user import User


@pytest.fixture()
async def app_config(tmp_path: PosixPath) -> None:
    config_path = tmp_path.joinpath("app.cfg")
    database_url = f"sqlite:///{tmp_path.as_posix()}/w2fm.db"
    with open(config_path, "w") as fh:
        fh.write(
            f"""
DATABASE__SQLALCHEMY__URL = "{database_url}"
LOGGING_CONFIG = "logging.yaml.example"
FASJSON_URL = "http://fasjson.example.com"
DATAGREPPER_URL = "http://datagrepper.example.com/"
"""
        )
    set_config_file(config_path.as_posix())


@pytest.fixture()
async def db(app_config: None) -> AsyncGenerator[AsyncDatabaseManager, None]:
    """
    For initializing the database
    """
    from webhook_to_fedora_messaging import models  # noqa: F401

    get_db_manager.cache_clear()
    db_mgr = get_db_manager()
    await db_mgr.sync()
    yield db_mgr


@pytest.fixture()
async def db_session(db: AsyncDatabaseManager) -> AsyncGenerator[AsyncSession, None]:
    """
    For initializing the database session
    """
    session = db.Session()
    with mock.patch("webhook_to_fedora_messaging.database.get_session") as get_session:
        get_session.return_value = session
        yield session
    await session.close()


@pytest.fixture()
async def client(app_config: None, db: AsyncDatabaseManager) -> AsyncGenerator[AsyncClient, None]:
    """
    For initializing the testing client
    """
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture()
async def db_user(client: AsyncClient, db_session: AsyncSession) -> AsyncGenerator[User, None]:
    """
    For seeding the database with user
    """
    # Setup code to create the object in the database
    user, is_created = await database.get_or_create(
        db_session, User, name="mehmet"
    )  # Adjust fields as necessary
    await db_session.commit()
    # Refreshing seems necessary on sqlite because it does not support timezones in timestamps
    await db_session.refresh(user)

    yield user

    # Teardown code to remove the object from the database
    await db_session.delete(user)
    await db_session.commit()


@pytest.fixture()
async def authenticated(db_user: User, client: AsyncClient) -> AsyncGenerator[mock.MagicMock, None]:
    """
    For authenticating the connected client
    """
    oidc_user = {
        "nickname": db_user.name,
        "email": f"{db_user.name}@example.com",
        "sub": "dummyusersub",
    }
    with mock.patch("webhook_to_fedora_messaging.auth.oauth") as oauth:
        oauth.fedora.userinfo = mock.AsyncMock(return_value=oidc_user)
        client.headers = Headers({"Authorization": "Bearer dummy-token"})
        yield oauth


@pytest.fixture()
async def db_service(
    client: AsyncClient, db_user: User, db_session: AsyncSession, request: pytest.FixtureRequest
) -> AsyncGenerator[Service, None]:
    """
    For seeding the database with service
    """
    service, created = await database.get_or_create(
        db_session,
        Service,
        name="Demo Service",
        type=request.param,
        desc="description",
    )

    service.token = "dummy-service-token"  # noqa: S105
    await db_session.flush()
    (await service.awaitable_attrs.users).append(db_user)
    await db_session.commit()

    # Refreshing seems necessary on sqlite because it does not support timezones in timestamps
    await db_session.refresh(service)

    yield service

    # Teardown code to remove the object from the database
    await db_session.delete(service)
    await db_session.commit()
