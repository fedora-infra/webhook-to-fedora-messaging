from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.session import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

from webhook_to_fedora_messaging.auth import user
from webhook_to_fedora_messaging.config import logger
from webhook_to_fedora_messaging.database import session
from webhook_to_fedora_messaging.endpoints.models.user import (
    UserExternal,
    UserManyResult,
    UserRequest,
    UserResult,
)
from webhook_to_fedora_messaging.models import User


router = APIRouter(prefix="/users")


@router.post("", status_code=HTTP_201_CREATED, response_model=UserResult, tags=["user"])
def create_user(
    data: UserRequest,
    session: Session = Depends(session),  # noqa : B008
):
    #  user: User = Depends(user)  # noqa : B008
    """
    Create a user with the requested attributes
    """
    made_user = User(
        uuid=uuid4().hex[0:8],
        username=data.username,
        is_admin=False
    )
    session.add(made_user)
    data = UserExternal.from_orm(made_user).dict()
    try:
        session.flush()
    except IntegrityError as expt:
        logger.logger_object.warning("Uniquness constraint failed - Please try again")
        logger.logger_object.warning(str(expt))
        raise HTTPException(HTTP_409_CONFLICT, "Uniquness constraint failed - Please try again") from expt  # noqa : E501
    return {"action": "post", "user": data}


@router.get("", status_code=HTTP_200_OK, response_model=UserResult, tags=["user"])
def get_user(
    data: UserRequest,
    session: Session = Depends(session),  # noqa : B008
):
    """
    Return the user with the specified username
    """
    query = select(User).filter_by(username=data.username).options(selectinload("*"))
    result = session.execute(query)
    data = result.scalar_one_or_none()
    if not data:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            f"User with the requested username '{data.username}' was not found"
        )
    return {"action": "get", "user": data}


@router.get("/search", status_code=HTTP_200_OK, response_model=UserManyResult, tags=["user"])
def search_user(
    data: UserRequest,
    session: Session = Depends(session)  # noqa : B008
):
    """
    Return the list of users matching the specified username
    """
    query = select(User).filter(User.username.like(data.username)).options(selectinload("*"))
    result = session.execute(query)
    data = result.scalar()
    return {"action": "get", "users": [indx for indx in data]}
