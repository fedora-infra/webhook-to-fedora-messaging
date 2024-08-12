# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, BasicAuth

from webhook_to_fedora_messaging import database
from webhook_to_fedora_messaging.config import setup_database_manager, standard
from webhook_to_fedora_messaging.main import create_app
from webhook_to_fedora_messaging.models.service import Service
from webhook_to_fedora_messaging.models.user import User


@pytest.fixture()
async def db(tmp_path):
    standard.database_url = f"sqlite:///{tmp_path.as_posix()}/w2fm.db"
    setup_database_manager()
    await database.db.sync()
    yield database.db


@pytest.fixture()
async def db_session(db):
    session = db.Session()
    yield session
    await session.close()


@pytest.fixture()
async def client(db):
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture()
async def db_user(client, db_session) -> AsyncGenerator[User, None]:
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
async def client_auth(db_user):
    return BasicAuth(username=db_user.name, password=db_user.name)


@pytest.fixture()
async def db_service(client, db_user, db_session) -> AsyncGenerator[Service, None]:
    service, created = await database.get_or_create(
        db_session,
        Service,
        name="GitHub Demo",
        type="github",
        desc="description",
        user_id=db_user.id,
    )

    service.token = "dummy-service-token"  # noqa: S105
    await db_session.commit()
    # Refreshing seems necessary on sqlite because it does not support timezones in timestamps
    await db_session.refresh(service)

    yield service

    # Teardown code to remove the object from the database
    await db_session.delete(service)
    await db_session.commit()
