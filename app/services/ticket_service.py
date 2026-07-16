from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from app.models import (
    Ticket,
    TicketPriority,
    TicketStatus,
)

from app.repositories import TicketRepository

from .base_service import BaseService


class TicketService(
    BaseService[Ticket],
):

    def __init__(
        self,
        repository: TicketRepository,
    ):
        super().__init__(repository)

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
    ) -> list[Ticket]:

        return self.repository.list_by_organization(
            organization_id,
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

    def archive(
        self,
        ticket_id: str,
    ) -> Ticket | None:

        ticket = self.get_by_id(ticket_id)

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