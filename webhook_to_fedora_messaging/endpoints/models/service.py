from abc import ABC
from datetime import datetime
from enum import Enum
from typing import Any, cast, Optional, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    HttpUrl,
    model_validator,
    ValidationError,
    ValidationInfo,
)
from starlette.requests import Request


class ServiceType(str, Enum):
    github = "github"
    forgejo = "forgejo"


class ServiceBase(BaseModel, ABC):
    """
    Base: Service
    """

    model_config = ConfigDict(from_attributes=True)
    uuid: str
    name: str
    type: ServiceType
    desc: str | None = None
    token: str
    creation_date: datetime


class ServiceExternal(ServiceBase):
    webhook_url: HttpUrl | None = None

    @model_validator(mode="after")
    def build_url(self, info: ValidationInfo) -> Self:
        if self.webhook_url is None and info.context is None:
            raise ValidationError("The request must be set in the context of model_validate()")
        request: Request = cast(dict[str, Any], info.context)["request"]
        self.webhook_url = HttpUrl(str(request.url_for("create_message", uuid=self.uuid)))
        return self


class ServiceInternal(ServiceBase):
    id: str


class ServiceRequestMain(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    type: ServiceType
    desc: Optional[str] = None


class ServiceRequest(BaseModel):
    data: ServiceRequestMain


class ServiceUpdateMain(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: Optional[str] = None
    type: Optional[str] = None
    desc: Optional[str] = None
    username: Optional[str] = None


class ServiceUpdate(BaseModel):
    data: ServiceUpdateMain


class ServiceResult(BaseModel):
    data: ServiceExternal


class ServiceManyResult(BaseModel):
    data: list[ServiceExternal] = []
