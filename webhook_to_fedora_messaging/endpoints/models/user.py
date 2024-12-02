from abc import ABC
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel, ABC):
    """
    Base: User
    """

    model_config = ConfigDict(from_attributes=True)
    name: str
    is_admin: bool = False
    creation_date: datetime


class UserExternal(UserBase):
    pass


class UserInternal(UserBase):
    id: str


class UserRequestMain(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str


class UserRequest(BaseModel):
    data: UserRequestMain


class UserResult(BaseModel):
    data: UserExternal


class UserManyResult(BaseModel):
    data: list[UserExternal] = []
