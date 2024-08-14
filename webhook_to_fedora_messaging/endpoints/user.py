import logging
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from webhook_to_fedora_messaging.auth import current_user
from webhook_to_fedora_messaging.database import get_session
from webhook_to_fedora_messaging.endpoints.models.user import (
    UserManyResult,
    UserRequest,
    UserResult,
)
from webhook_to_fedora_messaging.models import User


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users")


@router.post("", status_code=HTTP_201_CREATED, response_model=UserResult, tags=["users"])
async def create_user(
    body: UserRequest,
    session: AsyncSession = Depends(get_session),  # noqa : B008
    user: User = Depends(current_user),  # noqa : B008
):
    """
    Create a user with the requested attributes
    """
    made_user = User(username=body.data.name, uuid=uuid4().hex[0:8])
    session.add(made_user)
    try:
        await session.flush()
    except IntegrityError as expt:
        logger.exception("Uniqueness constraint failed")
        raise HTTPException(HTTP_409_CONFLICT, "Uniqueness constraint failed") from expt
    return {"data": made_user}


@router.get(
    "/search/{username}", status_code=HTTP_200_OK, response_model=UserManyResult, tags=["users"]
)
async def search_user(username: str, session: AsyncSession = Depends(get_session)):  # noqa : B008
    """
    Return the list of users matching the specified username
    """
    if username.strip() == "":
        raise HTTPException(HTTP_422_UNPROCESSABLE_ENTITY, "No lookup string provided")
    query = select(User).where(User.name.like(f"%{username}%"))
    result = await session.execute(query)
    return {"data": result.scalars().all()}


@router.get("/{username}", status_code=HTTP_200_OK, response_model=UserResult, tags=["users"])
async def get_user(
    username: str,
    session: AsyncSession = Depends(get_session),  # noqa : B008
):
    """
    Return the user with the specified username
    """
    if username.strip() == "":
        raise HTTPException(HTTP_422_UNPROCESSABLE_ENTITY, "No lookup string provided")
    query = select(User).filter_by(name=username).options(selectinload("*"))
    result = await session.execute(query)
    try:
        user_data = result.scalar_one()
    except NoResultFound as expt:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"User with the requested username '{username}' was not found"
        ) from expt
    return {"data": user_data}
