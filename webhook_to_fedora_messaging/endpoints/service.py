from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from webhook_to_fedora_messaging.auth import get_user
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
from webhook_to_fedora_messaging.endpoints.util import is_uuid_vacant


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
    user: User = Depends(get_user),  # noqa : B008
):
    """
    Create a service with the requested attributes
    """
    made_service = Service(
        name=body.name,
        uuid=uuid4().hex[0:8],
        type=body.type,
        desc=body.desc,
        user_id=user.id
    )
    session.add(made_service)
    try:
        await session.flush()
    except IntegrityError as expt:
        logger.logger_object.warning("Uniquness constraint failed - Please try again")
        logger.logger_object.warning(str(expt))
        raise HTTPException(HTTP_409_CONFLICT, "Uniquness constraint failed - Please try again") from expt  # noqa : E501
    return {
        "action": "post",
        "service": ServiceExternal.from_orm(made_service).dict()
    }


@router.get(
    "/list",
    status_code=HTTP_200_OK,
    response_model=ServiceManyResult,
    tags=["services"]
)
async def list_services(
    session: AsyncSession = Depends(get_session),  # noqa : B008
    user: User = Depends(get_user),  # noqa : B008
):
    """
    List all the services associated with a certain user
    """
    query = select(Service).where(Service.user_id==user.id)
    service_data = await session.scalars(query)
    return {
        "action": "get",
        "services": [ServiceExternal.from_orm(srvc).dict() for srvc in service_data]
    }


@router.get(
    "/{uuid}",
    status_code=HTTP_200_OK,
    response_model=ServiceResult,
    tags=["services"]
)
async def get_service(
    uuid: str = Depends(is_uuid_vacant),  # noqa : B008
    session: AsyncSession = Depends(get_session),  # noqa : B008
    user: User = Depends(get_user),  # noqa : B008
):
    """
    Return the service with the specified UUID
    """
    query = select(Service).filter_by(uuid=uuid).options(selectinload("*"))
    result = await session.execute(query)

    try:
        service_data = result.scalar_one()
    except NoResultFound as expt:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            f"Service with the requested UUID '{uuid}' was not found"
        ) from expt

    if service_data.user_id != user.id:
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            f"You are not permitted to view the service '{uuid}'"
        )

    return {
        "action": "get",
        "service": ServiceExternal.from_orm(service_data).dict()
    }


@router.put(
    "/revoke/{uuid}",
    status_code=HTTP_202_ACCEPTED,
    response_model=ServiceResult,
    tags=["services"]
)
async def revoke_service(
    uuid: str = Depends(is_uuid_vacant),  # noqa : B008
    session: AsyncSession = Depends(get_session),  # noqa : B008
    user: User = Depends(get_user),  # noqa : B008
):
    """
    Revoke the service with the specified UUID
    """
    query = select(Service).filter_by(uuid=uuid).options(selectinload("*"))
    result = await session.execute(query)

    try:
        service_data = result.scalar_one()
    except NoResultFound as expt:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            f"Service with the requested UUID '{uuid}' was not found"
        ) from expt

    if service_data.user_id != user.id:
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            f"You are not permitted to revoke the service '{uuid}'"
        )

    service_data.disabled = True
    await session.flush()

    return {
        "action": "put",
        "service": ServiceExternal.from_orm(service_data).dict()
    }


@router.put(
    "/{uuid}",
    status_code=HTTP_202_ACCEPTED,
    response_model=ServiceResult,
    tags=["services"]
)
async def update_service(
    body: ServiceUpdate,
    uuid: str = Depends(is_uuid_vacant),  # noqa : B008
    session: AsyncSession = Depends(get_session),  # noqa : B008
    user: User = Depends(get_user),  # noqa : B008
):
    """
    Update the service with the specified UUID
    """
    query = select(Service).filter_by(uuid=uuid).options(selectinload("*"))
    result = await session.execute(query)

    try:
        service_data = result.scalar_one()
    except NoResultFound as expt:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            "Service with the requested UUID '{uuid}' was not found"
        ) from expt

    if service_data.user_id != user.id:
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            f"You are not permitted to update the service '{uuid}'"
        )

    for attr in ("name", "type", "desc"):
        data = getattr(body, attr).strip()
        if not data:
            continue
        setattr(service_data, attr, data)

    if body.user_uuid.strip() != "":
        query = select(User).filter_by(uuid=body.user_uuid).options()
        result = await session.execute(query)
        try:
            user_data = result.scalar_one()
        except NoResultFound as expt:
            raise HTTPException(
                HTTP_422_UNPROCESSABLE_ENTITY,
                "Service was attempted to be transferred to a non-existent user"
            ) from expt
        service_data.user_id = user_data.id

    await session.flush()

    return {
        "action": "put",
        "service": ServiceExternal.from_orm(service_data).dict()
    }


@router.put(
    "/regenerate/{uuid}",
    status_code=HTTP_202_ACCEPTED,
    response_model=ServiceResult,
    tags=["services"]
)
async def regenerate_token(
    uuid: str = Depends(is_uuid_vacant),  # noqa : B008
    session: AsyncSession = Depends(get_session),  # noqa : B008
    user: User = Depends(get_user),  # noqa : B008
):
    """
    Regenerate the access token for the service with the requested UUID
    """
    query = select(Service).filter_by(uuid=uuid).options(selectinload("*"))
    result = await session.execute(query)

    try:
        service_data = result.scalar_one()
    except NoResultFound as expt:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            f"Service with the requested UUID '{uuid}' was not found"
        ) from expt

    if service_data.user_id != user.id:
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            f"You are not permitted to regenerate the access token for the service '{uuid}'"
        )

    service_data.token = uuid4().hex
    await session.flush()

    return {
        "action": "put",
        "service": service_data
    }
