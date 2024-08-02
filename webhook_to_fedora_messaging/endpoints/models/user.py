from abc import ABC
from datetime import datetime
from typing import List

from pydantic import BaseModel

from .common import APIResult


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


class UserRequest(BaseModel):
    username: str


class UserResult(APIResult):
    user: UserExternal


class UserManyResult(APIResult):
    users: List[UserExternal] = []
