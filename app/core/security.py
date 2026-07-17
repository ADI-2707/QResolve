from datetime import datetime, timedelta, timezone
from hashlib import sha256
import secrets

from argon2 import PasswordHasher
from jose import jwt

from app.core.config import (
    SECRET_KEY,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


PASSWORD_HASHER = PasswordHasher()


def new_secure_token() -> str:
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    return sha256(token.encode("utf-8")).hexdigest()


def hash_password(
    password: str,
) -> str:

    return PASSWORD_HASHER.hash(
        password
    )


def verify_password(
    password: str,
    password_hash: str,
) -> bool:

    try:

        PASSWORD_HASHER.verify(
            password_hash,
            password,
        )

        return True

    except Exception:

        return False


def create_access_token(
    subject: str,
    *,
    organization_id: str | None = None,
    organization_slug: str | None = None,
    role: str | None = None,
) -> str:

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": subject,
        "exp": expire,
    }

    if organization_id is not None:
        payload["organization_id"] = organization_id

    if organization_slug is not None:
        payload["organization_slug"] = organization_slug

    if role is not None:
        payload["role"] = role

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )
