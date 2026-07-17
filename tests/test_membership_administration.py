import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.models
from app.db.database import Base
from app.models import (
    Membership,
    MembershipRole,
    MembershipStatus,
    Organization,
    User,
    UserStatus,
)
from app.services.membership_administration_service import MembershipAdministrationService


def test_membership_administration_preserves_an_active_organization_admin():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    try:
        organization = Organization(name="Acme", slug="acme-members")
        db.add(organization)
        db.flush()
        admin_user = User(
            organization_id=organization.id,
            first_name="Ada",
            last_name="Admin",
            email="membership-admin@example.com",
            password_hash="not-used",
            status=UserStatus.ACTIVE,
        )
        agent_user = User(
            organization_id=organization.id,
            first_name="Alex",
            last_name="Agent",
            email="membership-agent@example.com",
            password_hash="not-used",
            status=UserStatus.ACTIVE,
        )
        db.add_all([admin_user, agent_user])
        db.flush()
        admin_membership = Membership(
            organization_id=organization.id,
            user_id=admin_user.id,
            role=MembershipRole.ORGANIZATION_ADMIN,
            status=MembershipStatus.ACTIVE,
        )
        agent_membership = Membership(
            organization_id=organization.id,
            user_id=agent_user.id,
            role=MembershipRole.AGENT,
            status=MembershipStatus.ACTIVE,
        )
        db.add_all([admin_membership, agent_membership])
        db.commit()

        service = MembershipAdministrationService(db)
        with pytest.raises(ValueError, match="at least one active administrator"):
            service.suspend(admin_membership)

        service.change_role(agent_membership, MembershipRole.ORGANIZATION_ADMIN)
        suspended_admin = service.suspend(admin_membership)

        assert suspended_admin.status == MembershipStatus.SUSPENDED
        assert agent_membership.role == MembershipRole.ORGANIZATION_ADMIN
        assert len(service.list_by_organization(organization.id)) == 2
    finally:
        db.close()
