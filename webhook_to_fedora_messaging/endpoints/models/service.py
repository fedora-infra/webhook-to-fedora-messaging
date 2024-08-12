from abc import ABC
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class ServiceType(str, Enum):
    github = "github"


class ServiceBase(BaseModel, ABC):
    """
    Base: Service
    """

    model_config = ConfigDict(from_attributes=True)


class ServiceExternal(ServiceBase):
    uuid: str
    name: str
    type: ServiceType
    desc: str
    token: str
    user_id: int
    creation_date: datetime


class ServiceInternal(ServiceExternal):
    id: str


class ServiceRequestMain(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    type: ServiceType
    desc: Optional[str]


class ServiceRequest(BaseModel):
    data: ServiceRequestMain


class ServiceUpdateMain(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: Optional[str] = ""
    type: Optional[str] = ""
    desc: Optional[str] = ""
    username: Optional[str] = ""


class ServiceUpdate(BaseModel):
    data: ServiceUpdateMain


class ServiceResult(BaseModel):
    data: ServiceExternal


class ServiceManyResult(BaseModel):
    data: List[ServiceExternal] = []
