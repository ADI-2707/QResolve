from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Department

from .base_repository import BaseRepository


class DepartmentRepository(BaseRepository[Department]):
    def __init__(self, db: Session):
        super().__init__(db=db, model=Department)

    def list_active(self, organization_id: str) -> list[Department]:
        return list(
            self.db.execute(
                select(Department)
                .where(
                    Department.organization_id == organization_id,
                    Department.archived_at.is_(None),
                )
                .order_by(Department.name.asc())
            )
            .scalars()
            .all()
        )

    def get_in_organization(self, department_id: str, organization_id: str) -> Department | None:
        return self.db.execute(
            select(Department).where(
                Department.id == department_id,
                Department.organization_id == organization_id,
                Department.archived_at.is_(None),
            )
        ).scalar_one_or_none()

    def exists_by_slug(self, organization_id: str, slug: str) -> bool:
        return self.db.execute(
            select(Department.id).where(
                Department.organization_id == organization_id,
                Department.slug == slug,
            )
        ).scalar_one_or_none() is not None
