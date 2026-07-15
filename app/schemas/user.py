from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import UserStatus


class UserCreate(BaseModel):

    organization_id: str

    first_name: str = Field(
        min_length=2,
        max_length=100,
    )

    last_name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
    )


class UserResponse(BaseModel):

    id: str

    organization_id: str

    first_name: str

    last_name: str

    email: EmailStr

    status: UserStatus

    created_at: datetime

    updated_at: datetime | None

    model_config = ConfigDict(
        from_attributes=True,
    )