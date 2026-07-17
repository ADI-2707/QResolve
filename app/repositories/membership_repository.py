from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    Membership,
    MembershipStatus,
    MembershipRole,
)

from .base_repository import BaseRepository


class MembershipRepository(
    BaseRepository[Membership],
):

    def __init__(
        self,
        db: Session,
    ):
        super().__init__(
            db=db,
            model=Membership,
        )

    def get_by_id(
        self,
        membership_id: str,
    ) -> Membership | None:

        statement = (
            select(Membership)
            .where(
                Membership.id == membership_id,
            )
        )

        return (
            self.db.execute(statement)
            .scalar_one_or_none()
        )

    def get_by_user(
        self,
        user_id: str,
    ) -> Membership | None:

        statement = (
            select(Membership)
            .where(
                Membership.user_id == user_id,
            )
        )

        return (
            self.db.execute(statement)
            .scalar_one_or_none()
        )

    def list_by_organization(
        self,
        organization_id: str,
    ) -> list[Membership]:

        statement = (
            select(Membership)
            .where(
                Membership.organization_id == organization_id,
            )
            .order_by(
                Membership.created_at.desc(),
            )
        )

        return list(
            self.db.execute(statement)
            .scalars()
            .all()
        )

    def list_active(
        self,
        organization_id: str,
    ) -> list[Membership]:

        statement = (
            select(Membership)
            .where(
                Membership.organization_id == organization_id,
                Membership.status == MembershipStatus.ACTIVE,
            )
        )

        return list(
            self.db.execute(statement)
            .scalars()
            .all()
        )

    def exists_platform_admin(
        self,
    ) -> bool:

        statement = (
            select(Membership)
            .where(
                Membership.role == MembershipRole.PLATFORM_ADMIN,
            )
            .limit(1)
        )

        return (
            self.db.execute(statement)
            .scalar_one_or_none()
            is not None
        )