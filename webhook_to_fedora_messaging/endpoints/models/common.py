from abc import ABC
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class APIResultAction(str, Enum):
    get = "get"
    post = "post"
    put = "put"
    delete = "delete"


class APIResult(BaseModel, ABC):
    action: Optional[APIResultAction]
