from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models import (
    TicketCategory,
    TicketPriority,
    TicketStatus,
)


class TicketCreate(BaseModel):

    subject: str = Field(
        min_length=3,
        max_length=255,
    )

    description: str = Field(
        min_length=10,
    )

    priority: TicketPriority = TicketPriority.MEDIUM

    category: TicketCategory = TicketCategory.OTHER


class TicketUpdate(BaseModel):

    subject: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        min_length=10,
    )

    status: TicketStatus | None = None

    priority: TicketPriority | None = None

    category: TicketCategory | None = None

    assigned_to: str | None = None


class TicketResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: str

    organization_id: str

    created_by: str

    assigned_to: str | None

    subject: str

    description: str

    status: TicketStatus

    priority: TicketPriority

    category: TicketCategory

    created_at: datetime

    updated_at: datetime

    archived_at: datetime | None


class TicketListResponse(BaseModel):

    tickets: list[TicketResponse]