from pydantic import BaseModel


class TicketAnalyticsResponse(BaseModel):
    total_tickets: int
    open_tickets: int
    in_progress_tickets: int
    resolved_tickets: int
    tickets_by_priority: dict[str, int]
    tickets_by_status: dict[str, int]
