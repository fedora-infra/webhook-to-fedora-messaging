import logging
from typing import Optional

from authlib.integrations.starlette_client import OAuth
from fastapi import Depends, HTTPException
from fastapi.security import OpenIdConnect
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED

from .config import get_config
from .database import get_or_create, get_session
from .models import User


log = logging.getLogger(__name__)

config = get_config()
metadata_url = f"{config.oidc.provider_url.rstrip('/')}/.well-known/openid-configuration"

oidc = OpenIdConnect(
    openIdConnectUrl=metadata_url,
    scheme_name="OpenID Connect",
)
oauth = OAuth()
oauth.register(
    "fedora",
    server_metadata_url=metadata_url,
    # client_id=standard.oidc_client_id,
    # client_kwargs={"scope": "openid email offline_access profile"},
    # client_secret=standard.oidc_client_secret,
)


class OIDCUser(BaseModel):
    nickname: str
    email: str
    name: str = None
    preferred_username: str = None
    groups: list[str] = Field(default_factory=list)
    sub: str


async def current_user(
    token: Optional[str] = Depends(oidc),
    session: AsyncSession = Depends(get_session),  # noqa : B008
):
    # Read the token
    try:
        token_type, token = token.split(" ", 1)
    except ValueError as e:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Can't read the token",
        ) from e
    if token_type.lower() != "bearer":
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Supplied token is not a Bearer token",
        )
    # Query user information
    try:
        userinfo = await oauth.fedora.userinfo(token={"access_token": token})
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=f"Supplied authentication could not be validated ({e})",
        ) from e
    oidc_user = OIDCUser(**userinfo)
    username = oidc_user.preferred_username or oidc_user.nickname
    # Add to the DB if needed
    user, created = await get_or_create(session, User, name=username)
    if created:
        log.info(f"User {username} logged in for the first time and was added to the database")
    else:
        log.info(f"User {username} logged in")
    return user
