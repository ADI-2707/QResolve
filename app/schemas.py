from pydantic import BaseModel, Field
from datetime import datetime


class TicketRequest(BaseModel):
    text: str = Field(
        ...,
        description="Complete support ticket text"
    )

    type: str = Field(
        ...,
        description="Ticket type"
    )

    queue: str = Field(
        ...,
        description="Support queue"
    )

    tag_1: str = Field(
        ...,
        description="Primary tag"
    )

    tag_2: str = "Unknown"
    tag_3: str = "Unknown"
    tag_4: str = "Unknown"


class PredictionResponse(BaseModel):
    priority: str


class PredictionHistoryResponse(BaseModel):

    id: int
    text: str
    type: str
    queue: str
    tag_1: str
    tag_2: str | None
    tag_3: str | None
    tag_4: str | None
    predicted_priority: str
    created_at: datetime

    class Config:
        from_attributes = True