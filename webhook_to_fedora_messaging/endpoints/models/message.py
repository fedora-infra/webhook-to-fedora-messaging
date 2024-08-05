from abc import ABC
from typing import Optional

from pydantic import BaseModel

from .common import APIResult


class MessageBase(BaseModel, ABC):
    """
    Base: Message
    """

    class Config:
        from_attributes = True


class MessageExternal(MessageBase):
    data: Optional[str]


class MessageRequest(BaseModel):
    data: Optional[str]


class MessageResult(APIResult):
    digest: str
