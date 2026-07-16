from datetime import datetime

from app.models import (
    Ticket,
    TicketStatus,
)

from app.repositories import TicketRepository


class TicketService:

    def __init__(
        self,
        repository: TicketRepository,
    ):
        self.repository = repository

    def create(
        self,
        ticket: Ticket,
    ) -> Ticket:

        ticket = self.repository.create(ticket)

        self.repository.db.commit()

        return ticket

    def get_by_id(
        self,
        ticket_id: str,
    ) -> Ticket | None:

        return self.repository.get_by_id(ticket_id)

    def list_by_organization(
        self,
        organization_id: str,
    ) -> list[Ticket]:

        return self.repository.list_by_organization(
            organization_id,
        )

    def list_by_status(
        self,
        organization_id: str,
        status,
    ) -> list[Ticket]:

        return self.repository.list_by_status(
            organization_id,
            status,
        )

    def list_by_priority(
        self,
        organization_id: str,
        priority,
    ) -> list[Ticket]:

        return self.repository.list_by_priority(
            organization_id,
            priority,
        )

    def list_by_assignee(
        self,
        organization_id: str,
        assignee_id: str,
    ) -> list[Ticket]:

        return self.repository.list_by_assignee(
            organization_id,
            assignee_id,
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

    def update(
        self,
        ticket: Ticket,
    ) -> Ticket:

        ticket = self.repository.update(ticket)

        self.repository.db.commit()

        return ticket

    def archive(
        self,
        ticket: Ticket,
    ) -> Ticket:

        ticket.status = TicketStatus.ARCHIVED
        ticket.archived_at = datetime.utcnow()

        ticket = self.repository.update(ticket)

        self.repository.db.commit()

        return ticket