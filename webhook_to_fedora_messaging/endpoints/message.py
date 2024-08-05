from fastapi import APIRouter, Depends, HTTPException, Request
from fedora_messaging import api
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.status import HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_ENTITY

from webhook_to_fedora_messaging.auth import get_user
from webhook_to_fedora_messaging.database import get_session
from webhook_to_fedora_messaging.endpoints.models.message import MessageRequest, MessageResult
from webhook_to_fedora_messaging.exceptions import SignatureMatchError
from webhook_to_fedora_messaging.models import Service, User

from .parser import parser


router = APIRouter(prefix="/messages")


@router.post(
    "/{uuid}",
    status_code=HTTP_202_ACCEPTED,
    response_model=MessageResult,
    tags=["messages"],
)
async def create_message(
    uuid: str,
    body: MessageRequest,
    request: Request,
    session: AsyncSession = Depends(get_session),  # noqa : B008
    user: User = Depends(get_user),  # noqa : B008
):
    """
    Create a message with the requested attributes
    """
    if uuid.strip() == "":
        raise HTTPException(HTTP_422_UNPROCESSABLE_ENTITY, "No service UUID provided")
    query = select(Service).filter_by(uuid=uuid).options(selectinload("*"))
    result = await session.execute(query)

    try:
        service_data = result.scalar_one()
    except NoResultFound as expt:
        raise HTTPException(
            HTTP_400_BAD_REQUEST,
            f"Service with the requested UUID '{uuid}' was not found"
        ) from expt

    try:
        message = parser(service_data, request.headers)
    except (SignatureMatchError, ValueError, KeyError) as expt:
        raise HTTPException(
            HTTP_400_BAD_REQUEST,
            f"Message could not be dispatched - {expt}"
        ) from expt

    api.publish(message)
    return {
        "action": "post",
        "uuid": message.id
    }
