import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from ..auth import current_user
from ..database import get_session
from ..models import User
from .models.user import (
    UserManyResult,
    UserResult,
)


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users")


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


@router.get("/me", status_code=HTTP_200_OK, response_model=UserResult, tags=["users"])
async def get_me(
    user: User = Depends(current_user),  # noqa : B008
):
    """
    Return the user with the specified username
    """
    return {"data": user}


@router.get("/{username}", status_code=HTTP_200_OK, response_model=UserResult, tags=["users"])
async def get_user(
    username: str,
    session: AsyncSession = Depends(get_session),  # noqa : B008
):
    """
    Return the user with the specified username
    """
    query = select(User).filter_by(name=username).options(selectinload("*"))
    result = await session.execute(query)
    try:
        user_data = result.scalar_one()
    except NoResultFound as expt:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"User with the requested username '{username}' was not found"
        ) from expt
    return {"data": user_data}
