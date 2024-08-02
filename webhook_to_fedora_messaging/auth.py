from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from webhook_to_fedora_messaging.database import get_session


def user_factory(optional: bool = False, **kwargs):
    """
    Factory creating FastAPI dependencies for authenticating users
    """
    if optional:
        kwargs["auto_error"] = False
    security = HTTPBasic(realm="W2FM", **kwargs)

    def user_actual(
        session: Session = Depends(get_session),  # noqa : B008
        cred: HTTPBasicCredentials = Security(security)  # noqa : B008
    ):
        if not cred:
            if not optional:
                raise HTTPException(HTTP_403_FORBIDDEN)
            else:
                return None
        username, password = cred.username, cred.password

        # Do not worry - This will be changed and we will request stuff from the database
        userlist = {
            "username": "password",
            "password": "username"
        }

        if username not in userlist:
            raise HTTPException(
                HTTP_401_UNAUTHORIZED,
                "Username not found"
            )

        if password != userlist[username]:
            raise HTTPException(
                HTTP_403_FORBIDDEN,
                "Invalid credentials"
            )

        return username, password

    return user_actual


user = user_factory()

user_optional = user_factory(optional=True)

