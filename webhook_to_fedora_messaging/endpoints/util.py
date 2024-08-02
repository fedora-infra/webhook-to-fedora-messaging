from fastapi import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def is_uuid_vacant(uuid) -> str:
    if uuid.strip() == "":
        raise HTTPException(HTTP_422_UNPROCESSABLE_ENTITY, "No service UUID provided")
    else:
        return uuid.strip()


