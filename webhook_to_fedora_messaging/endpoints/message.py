import logging
from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from fedora_messaging import exceptions as fm_exceptions
from starlette.status import HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_502_BAD_GATEWAY

from ..exceptions import SignatureMatchError
from ..models import Service
from ..publishing import publish
from .models.message import MessageResult
from .parser import parser
from .util import return_service_from_uuid, SerializedModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/messages")


@router.post(
    "/{uuid}",
    status_code=HTTP_202_ACCEPTED,
    response_model=MessageResult,
    tags=["messages"],
)
async def create_message(
    body: dict[str, Any],
    request: Request,
    background_tasks: BackgroundTasks,
    service: Service = Depends(return_service_from_uuid),  # noqa : B008
) -> SerializedModel:
    """
    Create a message with the requested attributes
    """
    if service.type == "pretix":
        background_tasks.add_task(_parse_and_send_message, service, request)
        return {"data": {"message_id": None}}
    message_id = await _parse_and_send_message(service, request)
    return {"data": {"message_id": message_id}}


async def _parse_and_send_message(service: Service, request: Request) -> str:
    try:
        message = await parser(service, request)
    except (SignatureMatchError, ValueError, KeyError) as expt:
        raise HTTPException(
            HTTP_400_BAD_REQUEST, f"Message could not be dispatched - {expt}"
        ) from expt

    try:
        await publish(message)
    except (fm_exceptions.ConnectionException, fm_exceptions.PublishException) as expt:
        logger.exception(
            "Could not send message %s for service %s (%s)", message.id, service.name, service.id
        )
        raise HTTPException(HTTP_502_BAD_GATEWAY, f"Message could not be sent: {expt}") from expt
    service.sent += 1
    return message.id
