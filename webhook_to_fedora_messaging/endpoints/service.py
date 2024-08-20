import logging
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from webhook_to_fedora_messaging.auth import current_user
from webhook_to_fedora_messaging.database import get_session
from webhook_to_fedora_messaging.endpoints.models.service import (
    ServiceManyResult,
    ServiceRequest,
    ServiceResult,
    ServiceUpdate,
)
from webhook_to_fedora_messaging.endpoints.util import authorized_service_from_uuid
from webhook_to_fedora_messaging.models import Service, User


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/services")


@router.post("", status_code=HTTP_201_CREATED, response_model=ServiceResult, tags=["services"])
async def create_service(
    body: ServiceRequest,
    session: AsyncSession = Depends(get_session),  # noqa : B008
    user: User = Depends(current_user),  # noqa : B008
):
    """
    Create a service with the requested attributes
    """
    made_service = Service(
        name=body.data.name,
        uuid=uuid4().hex[0:8],
        type=body.data.type,
        desc=body.data.desc,
    )
    session.add(made_service)
    try:
        await session.flush()
    except IntegrityError as expt:
        logger.exception("Uniqueness constraint failed")
        raise HTTPException(HTTP_409_CONFLICT, "This service already exists") from expt
    (await made_service.awaitable_attrs.users).append(user)
    return {"data": made_service}


@router.get("", status_code=HTTP_200_OK, response_model=ServiceManyResult, tags=["services"])
async def list_services(
    session: AsyncSession = Depends(get_session),  # noqa : B008
    user: User = Depends(current_user),  # noqa : B008
):
    """
    List all the services associated with a certain user
    """
    query = select(Service).where(Service.users.contains(user))
    service_data = await session.scalars(query)
    return {"data": service_data}


@router.get("/{uuid}", status_code=HTTP_200_OK, response_model=ServiceResult, tags=["services"])
async def get_service(
    session: AsyncSession = Depends(get_session),  # noqa : B008
    service: Service = Depends(authorized_service_from_uuid),  # noqa : B008
):
    """
    Return the service with the specified UUID
    """
    return {"data": service}


@router.put(
    "/{uuid}/revoke", status_code=HTTP_202_ACCEPTED, response_model=ServiceResult, tags=["services"]
)
async def revoke_service(
    session: AsyncSession = Depends(get_session),  # noqa : B008
    service: Service = Depends(authorized_service_from_uuid),  # noqa : B008
):
    """
    Revoke the service with the specified UUID
    """
    service.disabled = True
    await session.flush()
    return {"data": service}


@router.put(
    "/{uuid}", status_code=HTTP_202_ACCEPTED, response_model=ServiceResult, tags=["services"]
)
async def update_service(
    body: ServiceUpdate,
    session: AsyncSession = Depends(get_session),  # noqa : B008
    service: Service = Depends(authorized_service_from_uuid),  # noqa : B008
):
    """
    Update the service with the specified UUID
    """
    for attr in ("name", "type", "desc"):
        data = getattr(body.data, attr).strip()
        if not data:
            continue
        setattr(service, attr, data)

    if body.data.username.strip() != "":
        query = select(User).filter_by(name=body.data.username)
        result = await session.execute(query)
        try:
            user = result.scalar_one()
        except NoResultFound as expt:
            raise HTTPException(
                HTTP_422_UNPROCESSABLE_ENTITY,
                "Service was attempted to be transferred to a non-existent user",
            ) from expt
        if user not in service.users:
            service.users.append(user)

    await session.flush()

    return {"data": service}


@router.put(
    "/{uuid}/regenerate",
    status_code=HTTP_202_ACCEPTED,
    response_model=ServiceResult,
    tags=["services"],
)
async def regenerate_token(
    session: AsyncSession = Depends(get_session),  # noqa : B008
    service: Service = Depends(authorized_service_from_uuid),  # noqa : B008
):
    """
    Regenerate the access token for the service with the requested UUID
    """
    service.token = uuid4().hex
    await session.flush()
    return {"data": service}
