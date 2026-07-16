from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models import (
    Ticket,
    TicketPriority,
    TicketStatus,
)

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

        statement = (
            select(Ticket)
            .where(
                Ticket.organization_id == organization_id,
            )
            .order_by(
                Ticket.created_at.desc()
            )
        )

        return list(
            self.db.execute(statement)
            .scalars()
            .all()
        )

    def list_by_status(
        self,
        organization_id: str,
        status: TicketStatus,
    ) -> list[Ticket]:

        statement = (
            select(Ticket)
            .where(
                Ticket.organization_id == organization_id,
                Ticket.status == status,
            )
            .order_by(
                Ticket.created_at.desc()
            )
        )

        return list(
            self.db.execute(statement)
            .scalars()
            .all()
        )

    def list_by_priority(
        self,
        organization_id: str,
        priority: TicketPriority,
    ) -> list[Ticket]:

        statement = (
            select(Ticket)
            .where(
                Ticket.organization_id == organization_id,
                Ticket.priority == priority,
            )
            .order_by(
                Ticket.created_at.desc()
            )
        )

        return list(
            self.db.execute(statement)
            .scalars()
            .all()
        )

    def list_by_assignee(
        self,
        organization_id: str,
        assignee_id: str,
    ) -> list[Ticket]:

        statement = (
            select(Ticket)
            .where(
                Ticket.organization_id == organization_id,
                Ticket.assigned_to == assignee_id,
            )
            .order_by(
                Ticket.created_at.desc()
            )
        )

        return list(
            self.db.execute(statement)
            .scalars()
            .all()
        )

    def search(
        self,
        organization_id: str,
        query: str,
    ) -> list[Ticket]:

        statement = (
            select(Ticket)
            .where(
                Ticket.organization_id == organization_id,
            )
            .where(
                or_(
                    Ticket.subject.ilike(f"%{query}%"),
                    Ticket.description.ilike(f"%{query}%"),
                )
            )
            .order_by(
                Ticket.created_at.desc()
            )
        )

        return list(
            self.db.execute(statement)
            .scalars()
            .all()
        )