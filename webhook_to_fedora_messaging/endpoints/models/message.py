from abc import ABC
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    HttpUrl,
    model_validator,
)

from ...config import get_config


class MessageBase(BaseModel, ABC):
    """
    Base: Message
    """

    model_config = ConfigDict(from_attributes=True)


class MessageExternal(MessageBase):
    message_id: Optional[str]
    url: Optional[HttpUrl] = None

    @model_validator(mode="after")
    def build_url(self):
        base_url = get_config().datagrepper_url
        self.url = HttpUrl(f"{base_url}/v2/id?id={self.message_id}&is_raw=true&size=extra-large")
        return self


class MessageResult(BaseModel):
    data: MessageExternal
