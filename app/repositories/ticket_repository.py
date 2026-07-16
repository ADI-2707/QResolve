from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import Ticket
from app.models import TicketPriority
from app.models import TicketStatus
from app.repositories.base_repository import BaseRepository


class TicketRepository(BaseRepository[Ticket]):

    def __init__(
        self,
        db: Session,
    ):
        super().__init__(
            db=db,
            model=Ticket,
        )

    def list_by_organization(
        self,
        organization_id: str,
    ) -> list[Ticket]:

        return (
            self.db.query(Ticket)
            .filter(
                Ticket.organization_id == organization_id,
            )
            .all()
        )

    def list_by_status(
        self,
        organization_id: str,
        status: TicketStatus,
    ) -> list[Ticket]:

        return (
            self.db.query(Ticket)
            .filter(
                Ticket.organization_id == organization_id,
                Ticket.status == status,
            )
            .all()
        )

    def list_by_priority(
        self,
        organization_id: str,
        priority: TicketPriority,
    ) -> list[Ticket]:

        return (
            self.db.query(Ticket)
            .filter(
                Ticket.organization_id == organization_id,
                Ticket.priority == priority,
            )
            .all()
        )

    def list_by_assignee(
        self,
        organization_id: str,
        assignee_id: str,
    ) -> list[Ticket]:

        return (
            self.db.query(Ticket)
            .filter(
                Ticket.organization_id == organization_id,
                Ticket.assigned_to == assignee_id,
            )
            .all()
        )

    def search(
        self,
        organization_id: str,
        query: str,
    ) -> list[Ticket]:

        return (
            self.db.query(Ticket)
            .filter(
                Ticket.organization_id == organization_id,
            )
            .filter(
                or_(
                    Ticket.subject.ilike(f"%{query}%"),
                    Ticket.description.ilike(f"%{query}%"),
                )
            )
            .all()
        )