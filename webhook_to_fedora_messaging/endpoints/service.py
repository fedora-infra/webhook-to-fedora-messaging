from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

# from webhook_to_fedora_messaging.auth import user
from webhook_to_fedora_messaging.config import logger
from webhook_to_fedora_messaging.database import get_session
from webhook_to_fedora_messaging.endpoints.models.service import (
    ServiceExternal,
    ServiceManyResult,
    ServiceRequest,
    ServiceResult,
    ServiceUpdate,
)
from webhook_to_fedora_messaging.models import Service, User


router = APIRouter(prefix="/services")


@router.post(
    "",
    status_code=HTTP_201_CREATED,
    response_model=ServiceResult,
    tags=["services"]
)
async def create_service(
    body: ServiceRequest,
    session: AsyncSession = Depends(get_session),  # noqa : B008
):
    """
    Create a service with the requested attributes
    """
    query = select(User).filter_by(uuid=body.user_uuid).options(selectinload("*"))
    result = await session.execute(query)
    user_data = result.scalar_one_or_none()
    if not user_data:
        raise HTTPException(
            HTTP_422_UNPROCESSABLE_ENTITY,
            "Service cannot be associated with a non-existent user"
        )
    made_service = Service(
        name=body.name,
        uuid=uuid4().hex[0:8],
        type=body.type,
        desc=body.desc,
        user_id=user_data.id
    )
    session.add(made_service)
    try:
        await session.flush()
        data = ServiceExternal.from_orm(made_service).dict()
    except IntegrityError as expt:
        logger.logger_object.warning("Uniquness constraint failed - Please try again")
        logger.logger_object.warning(str(expt))
        raise HTTPException(HTTP_409_CONFLICT, "Uniquness constraint failed - Please try again") from expt  # noqa : E501
    return {
        "action": "post",
        "service": data
    }


@router.get(
    "/list/{uuid}",
    status_code=HTTP_200_OK,
    response_model=ServiceManyResult,
    tags=["services"]
)
async def list_services(
    uuid: str = "",
    session: AsyncSession = Depends(get_session),  # noqa : B008
):
    """
    List all the services associated with a certain user
    """
    if uuid.strip() == "":
        raise HTTPException(HTTP_422_UNPROCESSABLE_ENTITY, "No lookup string provided")
    query = select(User).filter_by(uuid=uuid).options(selectinload("*"))
    result = await session.execute(query)
    user_data = result.scalar_one_or_none()
    if not user_data:
        raise HTTPException(
            HTTP_422_UNPROCESSABLE_ENTITY,
            "Services associated with requested user cannot be found as the user does not exist"
        )
    query = select(Service).where(Service.user_id==user_data.id)
    result = await session.execute(query)
    service_data = result.scalars().all()
    return {
        "action": "get",
        "services": [ServiceExternal.from_orm(indx).dict() for indx in service_data]
    }


@router.get(
    "/{uuid}",
    status_code=HTTP_200_OK,
    response_model=ServiceResult,
    tags=["services"]
)
async def get_service(
    uuid: str,
    session: AsyncSession = Depends(get_session),  # noqa : B008
):
    """
    Return the service with the specified UUID
    """
    if uuid.strip() == "":
        raise HTTPException(HTTP_422_UNPROCESSABLE_ENTITY, "No lookup string provided")
    query = select(Service).filter_by(uuid=uuid).options(selectinload("*"))
    result = await session.execute(query)
    service_data = result.scalar_one_or_none()
    if not service_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            f"Service with the requested UUID '{uuid}' was not found"
        )
    return {
        "action": "get",
        "service": service_data
    }


@router.put(
    "/revoke/{uuid}",
    status_code=HTTP_202_ACCEPTED,
    response_model=ServiceResult,
    tags=["services"]
)
async def revoke_service(
    uuid: str,
    session: AsyncSession = Depends(get_session),  # noqa : B008
):
    """
    Revoke the service with the specified UUID
    """
    if uuid.strip() == "":
        raise HTTPException(HTTP_422_UNPROCESSABLE_ENTITY, "No lookup string provided")
    query = select(Service).filter_by(uuid=uuid).options(selectinload("*"))
    result = await session.execute(query)
    data = result.scalar_one_or_none()
    if not data:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            f"Service with the requested UUID '{uuid}' was not found"
        )
    data.disabled = True
    await session.flush()
    return {
        "action": "put",
        "service": data
    }


@router.put(
    "/{uuid}",
    status_code=HTTP_202_ACCEPTED,
    response_model=ServiceResult,
    tags=["services"]
)
async def update_service(
    body: ServiceUpdate,
    uuid: str,
    session: AsyncSession = Depends(get_session),  # noqa : B008
):
    """
    Update the service with the specified UUID
    """
    if uuid.strip() == "":
        raise HTTPException(HTTP_422_UNPROCESSABLE_ENTITY, "No lookup string provided")
    query = select(Service).filter_by(uuid=uuid).options(selectinload("*"))
    result = await session.execute(query)
    service_data = result.scalar_one_or_none()
    if not service_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            "Service with the requested UUID '{uuid}' was not found"
        )
    for attr in ("name", "type", "desc"):
        data = getattr(body, attr).strip()
        if not data:
            continue
        setattr(service_data, attr, data)
    if body.user_uuid.strip() != "":
        query = select(User).filter_by(uuid=body.user_uuid).options()
        result = await session.execute(query)
        user_data = result.scalar_one_or_none()
        if not user_data:
            raise HTTPException(
                HTTP_422_UNPROCESSABLE_ENTITY,
                "Service was attempted to be transferred to a non-existent user"
            )
        service_data.user_id = user_data.id
    await session.flush()
    return {
        "action": "put",
        "service": service_data
    }


@router.put(
    "/regenerate/{uuid}",
    status_code=HTTP_202_ACCEPTED,
    response_model=ServiceResult,
    tags=["services"]
)
async def regenerate_token(
    uuid: str,
    session: AsyncSession = Depends(get_session),  # noqa : B008
):
    """
    Regenerate the access token for the service with the requested UUID
    """
    if uuid.strip() == "":
        raise HTTPException(HTTP_422_UNPROCESSABLE_ENTITY, "No lookup string provided")
    query = select(Service).filter_by(uuid=uuid).options(selectinload("*"))
    result = await session.execute(query)
    service_data = result.scalar_one_or_none()
    if not service_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            "Service with the requested UUID '{uuid}' was not found"
        )
    service_data.token = uuid4().hex
    await session.flush()
    return {
        "action": "put",
        "service": service_data
    }
