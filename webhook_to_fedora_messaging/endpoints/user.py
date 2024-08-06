import logging
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

from webhook_to_fedora_messaging.auth import user_factory
from webhook_to_fedora_messaging.database import get_session
from webhook_to_fedora_messaging.endpoints.models.user import (
    UserExternal,
    UserManyResult,
    UserRequest,
    UserResult,
)
from webhook_to_fedora_messaging.models import User


logger = logging.getLogger(__name__)
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
    user: User = Depends(user_factory())  # noqa : B008
):
    """
    Create a user with the requested attributes
    """
    made_user = User(
        username=body.data.username,
        uuid=uuid4().hex[0:8]
    )
    session.add(made_user)
    try:
        await session.flush()
    except IntegrityError as expt:
        logger.exception("Uniqueness constraint failed")
        raise HTTPException(
            HTTP_409_CONFLICT,
            "Uniqueness constraint failed"
        ) from expt
    return {
        "data": UserExternal.model_validate(made_user).model_dump()
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
        "data": UserExternal.model_validate(user_data).model_dump()
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
    query = select(User).where(User.username.like(f"%{username}%"))
    result = await session.execute(query)
    return {
        "data": [UserExternal.model_validate(user).model_dump() for user in result.scalars().all()]
    }
