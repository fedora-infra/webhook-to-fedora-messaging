from abc import ABC
from typing import List, Optional

from pydantic import BaseModel

from .common import APIResult


class UserBase(BaseModel, ABC):
    """
    Base: User
    """

    class Config:
        from_attributes = True
        orm_mode = True


class UserExternal(UserBase):
    uuid: Optional[str] = ""
    username: Optional[str] = ""
    is_admin: bool = False
    creation_date: Optional[str]


class UserInternal(UserExternal):
    id: Optional[str] = ""


class UserRequest(BaseModel):
    username: str


class UserResult(APIResult):
    user: UserExternal


class UserManyResult(BaseModel):
    users: List[UserBase] = []
