from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Ticket, TicketStatus


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def ticket_overview(self, organization_id: str) -> dict:
        base_conditions = (
            Ticket.organization_id == organization_id,
            Ticket.status != TicketStatus.ARCHIVED,
        )
        total_tickets = self.db.execute(
            select(func.count()).select_from(Ticket).where(*base_conditions)
        ).scalar_one()
        status_rows = self.db.execute(
            select(Ticket.status, func.count())
            .where(*base_conditions)
            .group_by(Ticket.status)
        ).all()
        priority_rows = self.db.execute(
            select(Ticket.priority, func.count())
            .where(*base_conditions)
            .group_by(Ticket.priority)
        ).all()
        tickets_by_status = {status.value: count for status, count in status_rows}

        return {
            "total_tickets": total_tickets,
            "open_tickets": tickets_by_status.get(TicketStatus.OPEN.value, 0),
            "in_progress_tickets": tickets_by_status.get(TicketStatus.IN_PROGRESS.value, 0),
            "resolved_tickets": tickets_by_status.get(TicketStatus.RESOLVED.value, 0),
            "tickets_by_priority": {
                priority.value: count for priority, count in priority_rows
            },
            "tickets_by_status": tickets_by_status,
        }
