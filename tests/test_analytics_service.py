from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.models
from app.db.database import Base
from app.models import (
    Organization,
    Ticket,
    TicketCategory,
    TicketPriority,
    TicketStatus,
    User,
    UserStatus,
)
from app.services.analytics_service import AnalyticsService


def test_ticket_analytics_is_scoped_and_excludes_archived_tickets():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    try:
        organization = Organization(name="Acme", slug="acme-analytics")
        other_organization = Organization(name="Other", slug="other-analytics")
        db.add_all([organization, other_organization])
        db.flush()
        user = User(
            organization_id=organization.id,
            first_name="Ada",
            last_name="Agent",
            email="analytics-agent@example.com",
            password_hash="not-used",
            status=UserStatus.ACTIVE,
        )
        db.add(user)
        db.flush()
        db.add_all(
            [
                Ticket(
                    organization_id=organization.id,
                    created_by=user.id,
                    subject="Open issue",
                    description="An open support issue.",
                    priority=TicketPriority.HIGH,
                    category=TicketCategory.OTHER,
                    status=TicketStatus.OPEN,
                ),
                Ticket(
                    organization_id=organization.id,
                    created_by=user.id,
                    subject="Resolved issue",
                    description="A resolved support issue.",
                    priority=TicketPriority.LOW,
                    category=TicketCategory.OTHER,
                    status=TicketStatus.RESOLVED,
                ),
                Ticket(
                    organization_id=organization.id,
                    created_by=user.id,
                    subject="Archived issue",
                    description="An archived support issue.",
                    priority=TicketPriority.CRITICAL,
                    category=TicketCategory.OTHER,
                    status=TicketStatus.ARCHIVED,
                ),
            ]
        )
        db.commit()

        overview = AnalyticsService(db).ticket_overview(organization.id)

        assert overview["total_tickets"] == 2
        assert overview["open_tickets"] == 1
        assert overview["resolved_tickets"] == 1
        assert overview["tickets_by_priority"] == {"HIGH": 1, "LOW": 1}
    finally:
        db.close()
