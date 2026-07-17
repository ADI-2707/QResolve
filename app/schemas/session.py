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
