from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.models
from app.core.security import hash_password
from app.db.database import Base
from app.models import Organization, User, UserStatus
from app.repositories.audit_log_repository import AuditLogRepository
from app.services.audit_service import AuditService


def test_audit_service_persists_and_scopes_events_to_an_organization():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    try:
        organization = Organization(name="Acme", slug="acme-audit")
        db.add(organization)
        db.flush()
        user = User(
            organization_id=organization.id,
            first_name="Ada",
            last_name="Admin",
            email="audit-admin@example.com",
            password_hash=hash_password("SafePassword!123"),
            status=UserStatus.ACTIVE,
        )
        db.add(user)
        db.commit()

        event = AuditService(db).record(
            organization_id=organization.id,
            actor_id=user.id,
            action="TICKET_RESOLVED",
            entity_type="TICKET",
            entity_id="ticket-123",
            details={"resolution": "fixed"},
        )

        events = AuditLogRepository(db).list_by_organization(
            organization.id,
            page=1,
            page_size=25,
        )

        assert [item.id for item in events] == [event.id]
        assert events[0].details == {"resolution": "fixed"}
    finally:
        db.close()
