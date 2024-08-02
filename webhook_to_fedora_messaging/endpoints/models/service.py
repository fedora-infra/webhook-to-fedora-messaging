from abc import ABC
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .common import APIResult


class ServiceBase(BaseModel, ABC):
    """
    Base: Service
    """

    class Config:
        from_attributes = True


class ServiceExternal(ServiceBase):
    uuid: str
    name: str
    type: str
    desc: str
    token: str
    user_id: int
    creation_date: datetime


class ServiceInternal(ServiceExternal):
    id: str


class ServiceRequest(BaseModel):
    name: str
    type: str
    desc: Optional[str]


class ServiceUpdate(BaseModel):
    name: Optional[str] = ""
    type: Optional[str] = ""
    desc: Optional[str] = ""
    user_uuid: Optional[str] = ""


class ServiceResult(APIResult):
    service: ServiceExternal


class ServiceManyResult(APIResult):
    services: List[ServiceExternal] = []
