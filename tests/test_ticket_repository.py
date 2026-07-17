from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

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
from app.repositories.ticket_repository import TicketRepository
from app.repositories.user_repository import UserRepository
from app.services.ticket_service import TicketService


def build_repository() -> tuple[TicketRepository, Session, str, str]:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()

    organization = Organization(name="Acme", slug="acme")
    db.add(organization)
    db.flush()
    user = User(
        organization_id=organization.id,
        first_name="Ada",
        last_name="Admin",
        email="ticket-admin@example.com",
        password_hash="not-used-in-this-test",
        status=UserStatus.ACTIVE,
    )
    db.add(user)
    db.flush()
    return TicketRepository(db), db, organization.id, user.id


def add_ticket(
    db: Session,
    organization_id: str,
    user_id: str,
    subject: str,
    *,
    priority: TicketPriority = TicketPriority.MEDIUM,
    ticket_status: TicketStatus = TicketStatus.OPEN,
) -> Ticket:
    ticket = Ticket(
        organization_id=organization_id,
        created_by=user_id,
        subject=subject,
        description=f"Description for {subject}",
        priority=priority,
        category=TicketCategory.OTHER,
        status=ticket_status,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def test_ticket_listing_filters_searches_and_excludes_archived_records():
    repository, db, organization_id, user_id = build_repository()
    try:
        add_ticket(db, organization_id, user_id, "Login failure", priority=TicketPriority.HIGH)
        add_ticket(db, organization_id, user_id, "Billing question", priority=TicketPriority.LOW)
        add_ticket(
            db,
            organization_id,
            user_id,
            "Old login failure",
            ticket_status=TicketStatus.ARCHIVED,
        )

        tickets = repository.list_by_organization(
            organization_id,
            priority=TicketPriority.HIGH,
            search="login",
            page=1,
            page_size=25,
        )

        assert [ticket.subject for ticket in tickets] == ["Login failure"]
        assert repository.count_by_organization(organization_id) == 2
    finally:
        db.close()


def test_agent_claims_and_resolves_an_unassigned_ticket():
    repository, db, organization_id, user_id = build_repository()
    try:
        ticket = add_ticket(db, organization_id, user_id, "Password reset failure")
        service = TicketService(repository, UserRepository(db))

        claimed = service.claim(ticket.id, user_id)
        assert claimed.assigned_to == user_id
        assert claimed.status == TicketStatus.IN_PROGRESS

        resolved = service.resolve(
            ticket.id,
            user_id,
            may_resolve_any_ticket=False,
        )

        assert resolved.status == TicketStatus.RESOLVED
        assert resolved.resolved_at is not None
    finally:
        db.close()
