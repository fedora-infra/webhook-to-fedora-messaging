from abc import ABC
from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel, ABC):
    """
    Base: User
    """

    model_config = ConfigDict(from_attributes=True)


class UserExternal(UserBase):
    uuid: str
    name: str
    is_admin: bool = False
    creation_date: datetime


class UserInternal(UserExternal):
    id: str


class UserRequestMain(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str


class UserRequest(BaseModel):
    data: UserRequestMain


class UserResult(BaseModel):
    data: UserExternal


class UserManyResult(BaseModel):
    data: List[UserExternal] = []
