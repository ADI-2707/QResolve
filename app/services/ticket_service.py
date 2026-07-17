from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from app.models import (
    Ticket,
    TicketPriority,
    TicketStatus,
)

from app.repositories import (
    TicketRepository,
    UserRepository,
)

from .base_service import BaseService


class TicketService(BaseService[Ticket]):

    def __init__(
        self,
        repository: TicketRepository,
        user_repository: UserRepository,
    ):
        super().__init__(repository)
        self.user_repository = user_repository

    def create(
        self,
        ticket: Ticket,
    ) -> Ticket:

        return super().create(ticket)

    def get(
        self,
        ticket_id: str,
    ) -> Ticket | None:

        return self.get_by_id(ticket_id)

    def list_by_organization(
        self,
        organization_id: str,
        *,
        ticket_status: TicketStatus | None = None,
        priority: TicketPriority | None = None,
        search: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> list[Ticket]:

        return self.repository.list_by_organization(
            organization_id,
            ticket_status=ticket_status,
            priority=priority,
            search=search,
            page=page,
            page_size=page_size,
        )

    def count_by_organization(
        self,
        organization_id: str,
        *,
        ticket_status: TicketStatus | None = None,
        priority: TicketPriority | None = None,
        search: str | None = None,
    ) -> int:
        return self.repository.count_by_organization(
            organization_id,
            ticket_status=ticket_status,
            priority=priority,
            search=search,
        )

    def list_by_status(
        self,
        organization_id: str,
        status: TicketStatus,
    ) -> list[Ticket]:

        return self.repository.list_by_status(
            organization_id,
            status,
        )

    def list_by_priority(
        self,
        organization_id: str,
        priority: TicketPriority,
    ) -> list[Ticket]:

        return self.repository.list_by_priority(
            organization_id,
            priority,
        )

    def search(
        self,
        organization_id: str,
        query: str,
    ) -> list[Ticket]:

        return self.repository.search(
            organization_id,
            query,
        )

    def assign(
        self,
        ticket_id: str,
        assignee_id: str,
    ) -> Ticket:

        ticket = self.get(ticket_id)

        if ticket is None:
            raise ValueError("Ticket not found")

        assignee = self.user_repository.get_by_id(
            assignee_id,
        )

        if assignee is None:
            raise ValueError("User not found")

        if assignee.organization_id != ticket.organization_id:
            raise ValueError(
                "User belongs to another organization"
            )

        ticket.assigned_to = assignee.id

        ticket = self.repository.update(ticket)

        self.repository.db.commit()
        self.repository.db.refresh(ticket)

        return ticket

    def archive(
        self,
        ticket_id: str,
    ) -> Ticket | None:

        ticket = self.get(ticket_id)

        if ticket is None:
            return None

        try:

            ticket.status = TicketStatus.ARCHIVED
            ticket.archived_at = datetime.utcnow()

            ticket = self.repository.update(
                ticket,
            )

            self.repository.db.commit()
            self.repository.db.refresh(
                ticket,
            )

            return ticket

        except SQLAlchemyError:

            self.repository.db.rollback()
            raise
