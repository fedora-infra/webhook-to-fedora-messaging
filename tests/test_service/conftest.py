from collections.abc import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from webhook_to_fedora_messaging.models.service import Service
from webhook_to_fedora_messaging.models.user import User

from ..utils import make_db_service


@pytest.fixture()
async def db_service(
    client: AsyncClient, db_user: User, db_session: AsyncSession
) -> AsyncGenerator[Service]:
    service = await make_db_service(db_session, "github", db_user)
    yield service
    # Teardown code to remove the object from the database
    await db_session.delete(service)
    await db_session.commit()
