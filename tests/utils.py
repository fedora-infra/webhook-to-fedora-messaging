from sqlalchemy.ext.asyncio import AsyncSession

from webhook_to_fedora_messaging import database
from webhook_to_fedora_messaging.models.service import Service
from webhook_to_fedora_messaging.models.user import User


async def make_db_service(
    db_session: AsyncSession,
    service_type: str,
    db_user: User,
) -> Service:
    service, _created = await database.get_or_create(
        db_session,
        Service,
        name="Demo Service",
        type=service_type,
        desc="description",
    )

    service.token = "dummy-service-token"  # noqa: S105
    await db_session.flush()
    (await service.awaitable_attrs.users).append(db_user)
    await db_session.commit()

    # Refreshing seems necessary on sqlite because it does not support timezones in timestamps
    await db_session.refresh(service)

    return service
