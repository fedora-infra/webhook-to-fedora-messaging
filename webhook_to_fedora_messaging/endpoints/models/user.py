from abc import ABC
from datetime import datetime
from typing import List

from pydantic import BaseModel


class UserBase(BaseModel, ABC):
    """
    Base: User
    """

    class Config:
        from_attributes = True


class UserExternal(UserBase):
    uuid: str
    username: str
    is_admin: bool = False
    creation_date: datetime


class UserInternal(UserExternal):
    id: str


class UserRequestMain(BaseModel):
    username: str


class UserRequest(BaseModel):
    data: UserRequestMain


class UserResult(BaseModel):
    data: UserExternal


class UserManyResult(BaseModel):
    data: List[UserExternal] = []
