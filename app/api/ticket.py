from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user

from app.db.database import get_db

from app.models import (
    Ticket,
    User,
)

from app.repositories import TicketRepository

from app.schemas.ticket import (
    TicketCreate,
    TicketListResponse,
    TicketResponse,
    TicketUpdate,
)

from app.services import TicketService


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(
    payload: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    repository = TicketRepository(db)

    service = TicketService(repository)

    ticket = Ticket(
        organization_id=current_user.organization_id,
        created_by=current_user.id,
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
    current_user: User = Depends(get_current_user),
):

    repository = TicketRepository(db)

    service = TicketService(repository)

    tickets = service.list_by_organization(
        current_user.organization_id,
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
    current_user: User = Depends(get_current_user),
):

    repository = TicketRepository(db)

    service = TicketService(repository)

    ticket = service.get(ticket_id)

    if ticket is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    if ticket.organization_id != current_user.organization_id:

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
    current_user: User = Depends(get_current_user),
):

    repository = TicketRepository(db)

    service = TicketService(repository)

    ticket = service.get(ticket_id)

    if ticket is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    if ticket.organization_id != current_user.organization_id:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    update_data = payload.model_dump(
        exclude_unset=True,
    )

    for field, value in update_data.items():

        setattr(
            ticket,
            field,
            value,
        )

    return service.update(ticket)


@router.delete(
    "/{ticket_id}",
    response_model=TicketResponse,
)
def archive_ticket(
    ticket_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    repository = TicketRepository(db)

    service = TicketService(repository)

    ticket = service.get(ticket_id)

    if ticket is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    if ticket.organization_id != current_user.organization_id:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return service.archive(ticket_id)