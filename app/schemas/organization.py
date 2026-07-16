from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class OrganizationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    ARCHIVED = "ARCHIVED"


class OrganizationCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=150,
    )


class OrganizationResponse(BaseModel):
    id: str
    name: str
    slug: str
    status: OrganizationStatus

    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(
        from_attributes=True,
    )