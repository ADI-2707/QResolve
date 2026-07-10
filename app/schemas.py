from pydantic import BaseModel, Field


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