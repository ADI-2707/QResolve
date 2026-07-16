from sqlalchemy import select

from app.models import Organization

from .base_repository import BaseRepository


class OrganizationRepository(
    BaseRepository[Organization]
):

    def __init__(
        self,
        db,
    ):
        super().__init__(
            db=db,
            model=Organization,
        )


    def get_by_id(
        self,
        organization_id: str,
    ) -> Organization | None:

        statement = (
            select(Organization)
            .where(
                Organization.id == organization_id,
            )
        )

        return (
            self.db.execute(statement)
            .scalar_one_or_none()
        )


    def get_by_slug(
        self,
        slug: str,
    ) -> Organization | None:

        statement = (
            select(Organization)
            .where(
                Organization.slug == slug,
            )
        )

        return (
            self.db.execute(statement)
            .scalar_one_or_none()
        )


    def list(
        self,
    ) -> list[Organization]:

        statement = (
            select(Organization)
            .order_by(
                Organization.created_at.desc()
            )
        )

        return list(
            self.db.execute(statement)
            .scalars()
            .all()
        )


    def exists_by_slug(
        self,
        slug: str,
    ) -> bool:

        return (
            self.get_by_slug(slug)
            is not None
        )