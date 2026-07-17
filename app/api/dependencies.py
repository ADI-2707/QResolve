from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer

from jose import JWTError
from jose import jwt

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import (
    SECRET_KEY,
    JWT_ALGORITHM,
)

from app.db.database import get_db

from app.core.authorization import AuthenticatedSession
from app.models import (
    Membership,
    MembershipStatus,
    Organization,
    OrganizationStatus,
    User,
    UserStatus,
)

from app.repositories import UserRepository


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
)


def get_current_session(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> AuthenticatedSession:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

        user_id = payload.get("sub")
        organization_id = payload.get("organization_id")
        organization_slug = payload.get("organization_slug")
        role = payload.get("role")

        if not all([user_id, organization_id, organization_slug, role]):
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    repository = UserRepository(db)

    user = repository.get_by_id(user_id)

    if user is None or user.status != UserStatus.ACTIVE:
        raise credentials_exception

    organization = db.get(Organization, organization_id)

    if (
        organization is None
        or organization.status != OrganizationStatus.ACTIVE
        or organization.slug != organization_slug
        or user.organization_id != organization.id
    ):
        raise credentials_exception

    membership = db.execute(
        select(Membership).where(
            Membership.user_id == user.id,
            Membership.organization_id == organization.id,
            Membership.status == MembershipStatus.ACTIVE,
        )
    ).scalar_one_or_none()

    if membership is None or membership.role.value != role:
        raise credentials_exception

    return AuthenticatedSession(
        user=user,
        organization=organization,
        membership=membership,
    )


def get_current_user(
    session: AuthenticatedSession = Depends(get_current_session),
) -> User:
    """Compatibility dependency for handlers that only need the user model."""
    return session.user
