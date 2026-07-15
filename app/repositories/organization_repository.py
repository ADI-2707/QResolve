from app.models import Organization
from sqlalchemy import select
from .base_repository import BaseRepository


class OrganizationRepository(BaseRepository[Organization]):
    def __init__(self, db):
        super().__init__(
            db=db,
            model=Organization,
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

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    def exists_by_slug(
        self,
        slug: str,
    ) -> bool:

        return (
            self.get_by_slug(slug)
            is not None
        )