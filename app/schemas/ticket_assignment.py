from pydantic import BaseModel


class TicketAssignment(BaseModel):

    assignee_id: str