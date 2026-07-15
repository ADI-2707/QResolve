from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Organization


class OrganizationRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db


    def create(
        self,
        organization: Organization,
    ) -> Organization:

        self.db.add(organization)
        self.db.flush()
        self.db.refresh(organization)

        return organization


    def get_by_id(
        self,
        organization_id: str,
    ) -> Organization | None:

        statement = select(Organization).where(
            Organization.id == organization_id,
        )

        return self.db.scalar(statement)

    def get_by_slug(
        self,
        slug: str,
    ) -> Organization | None:

        statement = select(Organization).where(
            Organization.slug == slug,
        )

        return self.db.scalar(statement)

    def exists_by_slug(
        self,
        slug: str,
    ) -> bool:

        return self.get_by_slug(slug) is not None

    def list(
        self,
    ) -> list[Organization]:

        statement = (
            select(Organization)
            .order_by(Organization.created_at.desc())
        )

        return list(
            self.db.scalars(statement).all()
        )


    def update(
        self,
        organization: Organization,
    ) -> Organization:

        self.db.flush()
        self.db.refresh(organization)

        return organization