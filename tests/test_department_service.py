import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.models
from app.db.database import Base
from app.models import Organization
from app.repositories.department_repository import DepartmentRepository
from app.services.department_service import DepartmentService


def test_department_service_creates_unique_slugs_and_soft_archives_departments():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    try:
        organization = Organization(name="Acme", slug="acme-departments")
        db.add(organization)
        db.commit()

        service = DepartmentService(DepartmentRepository(db))
        first = service.create(organization.id, "Technical Support")
        second = service.create(organization.id, "Technical Support")
        archived = service.archive(first)

        assert first.slug == "technical-support"
        assert second.slug == "technical-support-2"
        assert archived.archived_at is not None
        assert archived.is_active is False
        assert [department.id for department in service.repository.list_active(organization.id)] == [second.id]
    finally:
        db.close()
