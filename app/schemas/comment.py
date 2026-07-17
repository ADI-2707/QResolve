from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentCreate(BaseModel):
    content: str = Field(min_length=1, max_length=10000)


class CommentResponse(BaseModel):
    id: str
    organization_id: str
    ticket_id: str
    user_id: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
