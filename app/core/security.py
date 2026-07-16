from datetime import datetime, timedelta, timezone

from argon2 import PasswordHasher
from jose import jwt

from app.core.config import (
    SECRET_KEY,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


PASSWORD_HASHER = PasswordHasher()


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

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )