from pydantic import BaseModel, Field

from typing import Optional


class ServiceCreate(BaseModel):
    username: str = Field(default=None, description="Username")
    type: str = Field(default=None, description="Type")
    desc: Optional[str] = Field(default=None, description="Description")
    name: str = Field(default=None, description="Name")


class ServiceSearch(BaseModel):
    service_uuid: str = Field(default=None, description="Service UUID")


class ServiceRevoke(BaseModel):
    service_uuid: str = Field(default=None, description="Service UUID")
    username: str = Field(default=None, description="Username")


class ServiceUpdate(BaseModel):
    service_uuid: str = Field(default=None, description="Service UUID")
    desc: Optional[str] = Field(default=None, description="Description")
    name: Optional[str] = Field(default=None, description="Name")


class RefreshToken(BaseModel):
    service_uuid: str = Field(default=None, description="Service UUID")
