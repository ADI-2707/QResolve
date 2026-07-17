from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TicketPredictionResponse(BaseModel):
    id: int
    ticket_id: str
    predicted_priority: str
    predicted_department: str | None
    confidence_score: float | None
    model_version: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
