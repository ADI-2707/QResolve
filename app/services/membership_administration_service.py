from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Membership, MembershipRole, MembershipStatus


class MembershipAdministrationService:
    def __init__(self, db: Session):
        self.db = db

    def list_by_organization(self, organization_id: str) -> list[Membership]:
        return list(
            self.db.execute(
                select(Membership)
                .where(
                    Membership.organization_id == organization_id,
                    Membership.status != MembershipStatus.ARCHIVED,
                )
                .order_by(Membership.created_at.asc())
            )
            .scalars()
            .all()
        )

    def get_in_organization(
        self,
        membership_id: str,
        organization_id: str,
    ) -> Membership | None:
        return self.db.execute(
            select(Membership).where(
                Membership.id == membership_id,
                Membership.organization_id == organization_id,
            )
        ).scalar_one_or_none()

    def change_role(
        self,
        membership: Membership,
        role: MembershipRole,
    ) -> Membership:
        self._validate_organization_role(role)
        if membership.role == MembershipRole.ORGANIZATION_ADMIN and role != membership.role:
            self._ensure_another_active_admin(membership.organization_id, membership.id)

        membership.role = role
        self.db.commit()
        self.db.refresh(membership)
        return membership

    def suspend(self, membership: Membership) -> Membership:
        if membership.status != MembershipStatus.ACTIVE:
            raise ValueError("Only active memberships can be suspended")
        if membership.role == MembershipRole.ORGANIZATION_ADMIN:
            self._ensure_another_active_admin(membership.organization_id, membership.id)

        membership.status = MembershipStatus.SUSPENDED
        self.db.commit()
        self.db.refresh(membership)
        return membership

    def activate(self, membership: Membership) -> Membership:
        if membership.status != MembershipStatus.SUSPENDED:
            raise ValueError("Only suspended memberships can be activated")

        membership.status = MembershipStatus.ACTIVE
        self.db.commit()
        self.db.refresh(membership)
        return membership

    def _ensure_another_active_admin(
        self,
        organization_id: str,
        excluded_membership_id: str,
    ) -> None:
        active_admins = self.db.execute(
            select(func.count()).select_from(Membership).where(
                Membership.organization_id == organization_id,
                Membership.role == MembershipRole.ORGANIZATION_ADMIN,
                Membership.status == MembershipStatus.ACTIVE,
                Membership.id != excluded_membership_id,
            )
        ).scalar_one()
        if active_admins == 0:
            raise ValueError("An organization must retain at least one active administrator")

    @staticmethod
    def _validate_organization_role(role: MembershipRole) -> None:
        if role == MembershipRole.PLATFORM_ADMIN:
            raise ValueError("Platform administrator is not an organization role")
