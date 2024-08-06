from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from webhook_to_fedora_messaging.auth import user_factory
from webhook_to_fedora_messaging.database import get_session
from webhook_to_fedora_messaging.models.service import Service
from webhook_to_fedora_messaging.models.user import User


async def is_uuid_vacant(uuid: str) -> str:
    if uuid.strip() == "":
        raise HTTPException(HTTP_422_UNPROCESSABLE_ENTITY, "No service UUID provided")
    return uuid.strip()


async def return_service_from_uuid(
    uuid: str = Depends(is_uuid_vacant),
    session: AsyncSession = Depends(get_session)  # noqa : B008
) -> Service:
    query = select(Service).filter_by(uuid=uuid).options(selectinload("*"))
    result = await session.execute(query)
    try:
        service = result.scalar_one()
    except NoResultFound as expt:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            f"Service with the requested UUID '{uuid}' was not found"
        ) from expt
    return service


async def authorized_service_from_uuid(
    service: Service = Depends(return_service_from_uuid),  # noqa : B008
    user: User = Depends(user_factory())  # noqa : B008
) -> Service:
    if service.user_id != user.id:
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            f"You are not permitted to access the service '{service.uuid}'"
        )
    return service
