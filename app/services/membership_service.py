from datetime import datetime

from app.models import (
    Membership,
    MembershipRole,
    MembershipStatus,
)

from app.repositories import MembershipRepository

from .base_service import BaseService


class MembershipService(
    BaseService[Membership],
):

    def __init__(
        self,
        repository: MembershipRepository,
    ):
        super().__init__(repository)

    def create(
        self,
        organization_id: str,
        user_id: str,
        role: MembershipRole,
        invited_by: str | None = None,
    ) -> Membership:

        membership = Membership(
            organization_id=organization_id,
            user_id=user_id,
            role=role,
            status=MembershipStatus.ACTIVE,
            invited_by=invited_by,
            joined_at=datetime.utcnow(),
            accepted_at=datetime.utcnow(),
        )

        return super().create(
            membership,
        )

    def get(
        self,
        membership_id: str,
    ) -> Membership | None:

        return self.get_by_id(
            membership_id,
        )

    def get_by_user(
        self,
        user_id: str,
    ) -> Membership | None:

        return self.repository.get_by_user(
            user_id,
        )

    def list_by_organization(
        self,
        organization_id: str,
    ) -> list[Membership]:

        return self.repository.list_by_organization(
            organization_id,
        )

    def archive(
        self,
        membership_id: str,
    ) -> Membership | None:

        membership = self.get(
            membership_id,
        )

        if membership is None:
            return None

        membership.status = MembershipStatus.ARCHIVED
        membership.archived_at = datetime.utcnow()

        self.repository.update(
            membership,
        )

        return membership