from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from webhook_to_fedora_messaging.database import get_session
from webhook_to_fedora_messaging.models import User


def user_factory(optional: bool = False, **kwargs):
    """
    Factory creating FastAPI dependencies for authenticating users
    """
    if optional:
        kwargs["auto_error"] = False
    security = HTTPBasic(realm="W2FM", **kwargs)

    async def user_actual(
        session: AsyncSession = Depends(get_session),  # noqa : B008
        cred: HTTPBasicCredentials = Security(security)  # noqa : B008
    ):
        if not cred:
            if not optional:
                raise HTTPException(HTTP_403_FORBIDDEN)
            else:
                return None
        username, password = cred.username, cred.password

        query = select(User).filter_by(username=username).options(selectinload("*"))
        result = await session.execute(query)

        try:
            user_data = result.scalar_one()
        except NoResultFound as expt:
            raise HTTPException(
                HTTP_401_UNAUTHORIZED,
                "Username not found"
            ) from expt

        # Do not worry - We will move on from basic HTTP authentication to OpenID Connect
        if password != username:
            raise HTTPException(
                HTTP_403_FORBIDDEN,
                "Invalid credentials"
            )

        return user_data

    return user_actual
