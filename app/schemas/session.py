from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class BootstrapRequest(BaseModel):
    organization_name: str = Field(min_length=2, max_length=150)
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=12)


class LoginPayload(BaseModel):
    organization_slug: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str


class SessionResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    organization_id: str
    organization_slug: str
    role: str


class InvitationCreate(BaseModel):
    email: EmailStr
    role: str = "AGENT"


class InvitationResponse(BaseModel):
    id: str
    email: EmailStr
    role: str
    expires_at: datetime
    invitation_token: str


class InvitationAcceptance(BaseModel):
    token: str = Field(min_length=32)
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=12)
