from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.models
from app.db.database import Base
from app.models import (
    Organization,
    Ticket,
    TicketCategory,
    TicketPriority,
    User,
    UserStatus,
)
from app.repositories.comment_repository import CommentRepository
from app.services.comment_service import CommentService


def test_comment_service_creates_and_lists_internal_ticket_comments():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    try:
        organization = Organization(name="Acme", slug="acme-comments")
        db.add(organization)
        db.flush()
        user = User(
            organization_id=organization.id,
            first_name="Ada",
            last_name="Agent",
            email="comments-agent@example.com",
            password_hash="not-used",
            status=UserStatus.ACTIVE,
        )
        db.add(user)
        db.flush()
        ticket = Ticket(
            organization_id=organization.id,
            created_by=user.id,
            subject="Login issue",
            description="The customer cannot sign in.",
            priority=TicketPriority.HIGH,
            category=TicketCategory.ACCOUNT,
        )
        db.add(ticket)
        db.commit()

        service = CommentService(CommentRepository(db))
        comment = service.create(
            organization_id=organization.id,
            ticket_id=ticket.id,
            user_id=user.id,
            content="Requested the account email address from the customer.",
        )

        comments = service.list_by_ticket(organization.id, ticket.id)

        assert [item.id for item in comments] == [comment.id]
        assert comments[0].content.startswith("Requested the account")
    finally:
        db.close()
