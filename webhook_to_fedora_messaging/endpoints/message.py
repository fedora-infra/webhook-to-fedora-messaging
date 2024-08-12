from fastapi import APIRouter, Depends, HTTPException, Request
from fedora_messaging import api
from starlette.status import HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST

from webhook_to_fedora_messaging.endpoints.models.message import MessageResult
from webhook_to_fedora_messaging.endpoints.util import return_service_from_uuid
from webhook_to_fedora_messaging.exceptions import SignatureMatchError
from webhook_to_fedora_messaging.models import Service

from .parser import parser


router = APIRouter(prefix="/messages")


@router.post(
    "/{uuid}",
    status_code=HTTP_202_ACCEPTED,
    response_model=MessageResult,
    tags=["messages"],
)
async def create_message(
    body: dict,
    request: Request,
    service: Service = Depends(return_service_from_uuid),  # noqa : B008
):
    """
    Create a message with the requested attributes
    """
    try:
        message = await parser(service, request)
    except (SignatureMatchError, ValueError, KeyError) as expt:
        raise HTTPException(
            HTTP_400_BAD_REQUEST, f"Message could not be dispatched - {expt}"
        ) from expt

    api.publish(message)
    return {"data": {"message_id": message.id}}
