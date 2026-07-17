from sqlalchemy import func, or_, select
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
        *,
        ticket_status: TicketStatus | None = None,
        priority: TicketPriority | None = None,
        search: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> list[Ticket]:
        statement = select(Ticket).where(
            *self._list_conditions(
                organization_id=organization_id,
                ticket_status=ticket_status,
                priority=priority,
                search=search,
            )
        ).order_by(Ticket.created_at.desc())

        if page is not None and page_size is not None:
            statement = statement.offset((page - 1) * page_size).limit(page_size)

        return list(
            self.db.execute(statement)
            .scalars()
            .all()
        )

    def count_by_organization(
        self,
        organization_id: str,
        *,
        ticket_status: TicketStatus | None = None,
        priority: TicketPriority | None = None,
        search: str | None = None,
    ) -> int:
        statement = select(func.count()).select_from(Ticket).where(
            *self._list_conditions(
                organization_id=organization_id,
                ticket_status=ticket_status,
                priority=priority,
                search=search,
            )
        )
        return self.db.execute(statement).scalar_one()

    @staticmethod
    def _list_conditions(
        *,
        organization_id: str,
        ticket_status: TicketStatus | None,
        priority: TicketPriority | None,
        search: str | None,
    ) -> list:
        conditions = [
            Ticket.organization_id == organization_id,
            Ticket.status != TicketStatus.ARCHIVED,
        ]
        if ticket_status is not None:
            conditions.append(Ticket.status == ticket_status)
        if priority is not None:
            conditions.append(Ticket.priority == priority)
        if search and search.strip():
            query = search.strip()
            conditions.append(
                or_(
                    Ticket.subject.ilike(f"%{query}%"),
                    Ticket.description.ilike(f"%{query}%"),
                )
            )
        return conditions

    def list_by_status(
        self,
        organization_id: str,
        status: TicketStatus,
    ) -> list[Ticket]:

        return self.list_by_organization(
            organization_id,
            ticket_status=status,
        )

    def list_by_priority(
        self,
        organization_id: str,
        priority: TicketPriority,
    ) -> list[Ticket]:

        return self.list_by_organization(
            organization_id,
            priority=priority,
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

        return self.list_by_organization(
            organization_id,
            search=query,
        )
