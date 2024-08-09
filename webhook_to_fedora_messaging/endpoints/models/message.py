from abc import ABC
from typing import Optional

from pydantic import BaseModel


class MessageBase(BaseModel, ABC):
    """
    Base: Message
    """

    class Config:
        from_attributes = True


class MessageExternal(MessageBase):
    data: Optional[str]


class MessageUUID(BaseModel):
    uuid: Optional[str]


class MessageResult(BaseModel):
    data: MessageUUID
