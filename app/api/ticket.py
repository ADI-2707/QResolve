from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.api.dependencies import get_current_session
from app.core.authorization import AuthenticatedSession, require_role
from app.db.database import get_db

from app.models import (
    Ticket,
    MembershipRole,
)

from app.repositories import (
    TicketRepository,
    UserRepository,
)

from app.schemas.ticket import (
    TicketCreate,
    TicketListResponse,
    TicketResponse,
    TicketUpdate,
)

from app.schemas.ticket_assignment import (
    TicketAssignment,
)

from app.services import TicketService


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


def get_ticket_service(
    db: Session,
) -> TicketService:

    ticket_repository = TicketRepository(db)
    user_repository = UserRepository(db)

    return TicketService(
        ticket_repository,
        user_repository,
    )


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(
    payload: TicketCreate,
    db: Session = Depends(get_db),
    session: AuthenticatedSession = Depends(get_current_session),
):
    require_role(session, MembershipRole.ORGANIZATION_ADMIN, MembershipRole.MANAGER, MembershipRole.AGENT)

    service = get_ticket_service(db)

    ticket = Ticket(
        organization_id=session.organization.id,
        created_by=session.user.id,
        subject=payload.subject,
        description=payload.description,
        priority=payload.priority,
        category=payload.category,
    )

    return service.create(ticket)


@router.get(
    "",
    response_model=TicketListResponse,
)
def list_tickets(
    db: Session = Depends(get_db),
    session: AuthenticatedSession = Depends(get_current_session),
):

    service = get_ticket_service(db)

    tickets = service.list_by_organization(
        session.organization.id,
    )

    return TicketListResponse(
        tickets=tickets,
    )


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse,
)
def get_ticket(
    ticket_id: str,
    db: Session = Depends(get_db),
    session: AuthenticatedSession = Depends(get_current_session),
):

    service = get_ticket_service(db)

    ticket = service.get(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    if ticket.organization_id != session.organization.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return ticket


@router.patch(
    "/{ticket_id}",
    response_model=TicketResponse,
)
def update_ticket(
    ticket_id: str,
    payload: TicketUpdate,
    db: Session = Depends(get_db),
    session: AuthenticatedSession = Depends(get_current_session),
):

    service = get_ticket_service(db)

    ticket = service.get(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    if ticket.organization_id != session.organization.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    update_data = payload.model_dump(
        exclude_unset=True,
    )

    if session.role == MembershipRole.VIEWER:
        require_role(session, MembershipRole.ORGANIZATION_ADMIN)
    if session.role == MembershipRole.AGENT:
        if ticket.assigned_to != session.user.id or set(update_data) - {"status"}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Agents may only update the status of tickets assigned to them",
            )

    for field, value in update_data.items():
        setattr(
            ticket,
            field,
            value,
        )

    ticket = service.update(ticket)

    db.commit()
    db.refresh(ticket)

    return ticket


@router.delete(
    "/{ticket_id}",
    response_model=TicketResponse,
)
def archive_ticket(
    ticket_id: str,
    db: Session = Depends(get_db),
    session: AuthenticatedSession = Depends(get_current_session),
):
    require_role(session, MembershipRole.ORGANIZATION_ADMIN)

    service = get_ticket_service(db)

    ticket = service.get(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    if ticket.organization_id != session.organization.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return service.archive(ticket_id)


@router.patch(
    "/{ticket_id}/assign",
    response_model=TicketResponse,
)
def assign_ticket(
    ticket_id: str,
    payload: TicketAssignment,
    db: Session = Depends(get_db),
    session: AuthenticatedSession = Depends(get_current_session),
):
    require_role(session, MembershipRole.ORGANIZATION_ADMIN, MembershipRole.MANAGER)

    service = get_ticket_service(db)

    ticket = service.get(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    if ticket.organization_id != session.organization.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    try:
        return service.assign(
            ticket_id,
            payload.assignee_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )
