from abc import ABC
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MessageBase(BaseModel, ABC):
    """
    Base: Message
    """

    model_config = ConfigDict(from_attributes=True)


class MessageExternal(MessageBase):
    message_id: Optional[str]


class MessageResult(BaseModel):
    data: MessageExternal
