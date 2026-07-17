import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import app.models
from app.api.dependencies import get_current_session
from app.core.security import create_access_token, hash_password
from app.db.database import Base
from app.models import (
    Membership,
    MembershipRole,
    MembershipStatus,
    Organization,
    User,
    UserStatus,
)
from app.services.invitation_service import InvitationService


@pytest.fixture
def db() -> Session:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


def create_active_admin(db: Session) -> tuple[Organization, User, Membership]:
    organization = Organization(name="Acme Support", slug="acme-support")
    db.add(organization)
    db.flush()

    user = User(
        organization_id=organization.id,
        first_name="Ada",
        last_name="Admin",
        email="ada@example.com",
        password_hash=hash_password("SafePassword!123"),
        status=UserStatus.ACTIVE,
    )
    db.add(user)
    db.flush()

    membership = Membership(
        organization_id=organization.id,
        user_id=user.id,
        role=MembershipRole.ORGANIZATION_ADMIN,
        status=MembershipStatus.ACTIVE,
    )
    db.add(membership)
    db.commit()
    return organization, user, membership


def test_current_session_uses_authoritative_membership_role(db: Session):
    organization, user, membership = create_active_admin(db)
    token = create_access_token(
        user.id,
        organization_id=organization.id,
        organization_slug=organization.slug,
        role=membership.role.value,
    )

    session = get_current_session(token=token, db=db)

    assert session.user.id == user.id
    assert session.organization.id == organization.id
    assert session.role == MembershipRole.ORGANIZATION_ADMIN

    forged_role_token = create_access_token(
        user.id,
        organization_id=organization.id,
        organization_slug=organization.slug,
        role=MembershipRole.AGENT.value,
    )

    with pytest.raises(HTTPException) as error:
        get_current_session(token=forged_role_token, db=db)

    assert error.value.status_code == 401


def test_invitation_acceptance_creates_single_active_membership(db: Session):
    organization, inviter, _ = create_active_admin(db)
    service = InvitationService(db)

    invitation, token = service.create(
        organization_id=organization.id,
        email="agent@example.com",
        role=MembershipRole.AGENT,
        invited_by=inviter.id,
    )
    user, membership = service.accept(
        token=token,
        first_name="Alex",
        last_name="Agent",
        password="AnotherSafePassword!123",
    )

    assert invitation.token_hash != token
    assert user.status == UserStatus.ACTIVE
    assert membership.organization_id == organization.id
    assert membership.role == MembershipRole.AGENT
    assert membership.status == MembershipStatus.ACTIVE

    with pytest.raises(ValueError, match="invalid or expired"):
        service.accept(
            token=token,
            first_name="Alex",
            last_name="Agent",
            password="AnotherSafePassword!123",
        )
