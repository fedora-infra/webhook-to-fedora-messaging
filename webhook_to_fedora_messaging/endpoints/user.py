from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

# from webhook_to_fedora_messaging.auth import user
from webhook_to_fedora_messaging.config import logger
from webhook_to_fedora_messaging.database import get_session
from webhook_to_fedora_messaging.endpoints.models.user import (
    UserExternal,
    UserManyResult,
    UserRequest,
    UserResult,
)
from webhook_to_fedora_messaging.models import User


router = APIRouter(prefix="/users")


@router.post(
    "",
    status_code=HTTP_201_CREATED,
    response_model=UserResult,
    tags=["users"]
)
async def create_user(
    body: UserRequest,
    session: AsyncSession = Depends(get_session),  # noqa : B008
):
    #  user: User = Depends(user)  # : B008
    """
    Create a user with the requested attributes
    """
    made_user = User(
        username=body.username,
        uuid=uuid4().hex[0:8]
    )
    session.add(made_user)
    try:
        await session.flush()
    except IntegrityError as expt:
        logger.logger_object.warning("Uniquness constraint failed - Please try again")
        logger.logger_object.warning(str(expt))
        raise HTTPException(HTTP_409_CONFLICT, "Uniquness constraint failed - Please try again") from expt  # noqa : E501
    return {
        "action": "post",
        "user": UserExternal.from_orm(made_user).dict()
    }


@router.get(
    "/{username}",
    status_code=HTTP_200_OK,
    response_model=UserResult,
    tags=["users"]
)
async def get_user(
    username: str,
    session: AsyncSession = Depends(get_session),  # noqa : B008
):
    """
    Return the user with the specified username
    """
    if username.strip() == "":
        raise HTTPException(HTTP_422_UNPROCESSABLE_ENTITY, "No lookup string provided")
    query = select(User).filter_by(username=username).options(selectinload("*"))
    result = await session.execute(query)
    user_data = result.scalar_one_or_none()
    if not user_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            f"User with the requested username '{username}' was not found"
        )
    return {
        "action": "get",
        "user": UserExternal.from_orm(user_data).dict()
    }


@router.get(
    "/search/{username}",
    status_code=HTTP_200_OK,
    response_model=UserManyResult,
    tags=["users"]
)
async def search_user(
    username: str,
    session: AsyncSession = Depends(get_session)  # noqa : B008
):
    """
    Return the list of users matching the specified username
    """
    if username.strip() == "":
        raise HTTPException(HTTP_422_UNPROCESSABLE_ENTITY, "No lookup string provided")
    query = select(User).where(User.username.like(f"%{username}%")).options(selectinload("*"))
    result = await session.execute(query)
    user_data = result.scalars().all()
    return {
        "action": "get",
        "users": [UserExternal.from_orm(indx).dict() for indx in user_data]
    }
