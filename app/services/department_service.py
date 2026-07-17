from datetime import datetime

from slugify import slugify
from sqlalchemy.exc import SQLAlchemyError

from app.models import Department
from app.repositories.department_repository import DepartmentRepository


class DepartmentService:
    def __init__(self, repository: DepartmentRepository):
        self.repository = repository

    def create(self, organization_id: str, name: str) -> Department:
        base_slug = slugify(name)
        if not base_slug:
            raise ValueError("Department name cannot generate a valid slug")
        slug = base_slug
        suffix = 2
        while self.repository.exists_by_slug(organization_id, slug):
            slug = f"{base_slug}-{suffix}"
            suffix += 1

        try:
            department = Department(organization_id=organization_id, name=name, slug=slug)
            self.repository.db.add(department)
            self.repository.db.commit()
            self.repository.db.refresh(department)
            return department
        except SQLAlchemyError:
            self.repository.db.rollback()
            raise

    def archive(self, department: Department) -> Department:
        department.is_active = False
        department.archived_at = datetime.utcnow()
        self.repository.db.commit()
        self.repository.db.refresh(department)
        return department
