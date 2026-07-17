from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class LoginRequest(BaseModel):

    email: EmailStr

    password: str


class BootstrapRequest(BaseModel):

    organization_name: str = Field(
        min_length=2,
        max_length=150,
    )

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


class TokenResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"