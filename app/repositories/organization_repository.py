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

        return (
            self.db.query(Organization)
            .filter(
                Organization.id == organization_id,
            )
            .first()
        )

    def get_by_slug(
        self,
        slug: str,
    ) -> Organization | None:

        return (
            self.db.query(Organization)
            .filter(
                Organization.slug == slug,
            )
            .first()
        )

    def exists_by_slug(
        self,
        slug: str,
    ) -> bool:

        return (
            self.db.query(Organization)
            .filter(
                Organization.slug == slug,
            )
            .first()
            is not None
        )

    def list(
        self,
    ) -> list[Organization]:

        return (
            self.db.query(Organization)
            .order_by(
                Organization.created_at.desc(),
            )
            .all()
        )


    def update(
        self,
        organization: Organization,
    ) -> Organization:

        self.db.flush()
        self.db.refresh(organization)

        return organization