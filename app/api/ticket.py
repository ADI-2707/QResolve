from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Query,
)

from sqlalchemy.orm import Session

from app.api.dependencies import get_current_session
from app.core.authorization import AuthenticatedSession, require_role
from app.db.database import get_db

from app.models import (
    Ticket,
    MembershipRole,
    TicketPriority,
    TicketStatus,
)

from app.repositories import (
    TicketRepository,
    UserRepository,
)
from app.repositories.department_repository import DepartmentRepository

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
from app.services.audit_service import AuditService
from app.services.ticket_prediction_service import TicketPredictionService
from app.schemas.ticket_prediction import TicketPredictionResponse
from app.schemas.ticket_prediction import TicketPredictionOverride
from app.models import Prediction


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
        department_id=_validated_department_id(
            db,
            payload.department_id,
            session.organization.id,
        ),
    )

    ticket = service.create(ticket)
    _record_ticket_event(
        db,
        session,
        action="TICKET_CREATED",
        ticket=ticket,
        details={"priority": ticket.priority.value, "category": ticket.category.value},
    )
    return ticket


@router.get(
    "",
    response_model=TicketListResponse,
)
def list_tickets(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    ticket_status: TicketStatus | None = Query(default=None, alias="status"),
    priority: TicketPriority | None = Query(default=None),
    search: str | None = Query(default=None, min_length=1, max_length=255),
    db: Session = Depends(get_db),
    session: AuthenticatedSession = Depends(get_current_session),
):

    service = get_ticket_service(db)

    tickets = service.list_by_organization(
        session.organization.id,
        ticket_status=ticket_status,
        priority=priority,
        search=search,
        page=page,
        page_size=page_size,
    )

    total_items = service.count_by_organization(
        session.organization.id,
        ticket_status=ticket_status,
        priority=priority,
        search=search,
    )

    return TicketListResponse(
        tickets=tickets,
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=(total_items + page_size - 1) // page_size,
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

    if update_data.get("department_id") is not None:
        update_data["department_id"] = _validated_department_id(
            db,
            update_data["department_id"],
            session.organization.id,
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

    _record_ticket_event(
        db,
        session,
        action="TICKET_UPDATED",
        ticket=ticket,
        details={"updated_fields": sorted(update_data)},
    )

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

    archived_ticket = service.archive(ticket_id)
    _record_ticket_event(
        db,
        session,
        action="TICKET_ARCHIVED",
        ticket=archived_ticket,
    )
    return archived_ticket


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
        assigned_ticket = service.assign(
            ticket_id,
            payload.assignee_id,
        )
        _record_ticket_event(
            db,
            session,
            action="TICKET_ASSIGNED",
            ticket=assigned_ticket,
            details={"assignee_id": assigned_ticket.assigned_to},
        )
        return assigned_ticket

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


@router.post(
    "/{ticket_id}/claim",
    response_model=TicketResponse,
)
def claim_ticket(
    ticket_id: str,
    db: Session = Depends(get_db),
    session: AuthenticatedSession = Depends(get_current_session),
):
    require_role(
        session,
        MembershipRole.ORGANIZATION_ADMIN,
        MembershipRole.MANAGER,
        MembershipRole.AGENT,
    )
    service = get_ticket_service(db)
    ticket = service.get(ticket_id)

    if ticket is None or ticket.organization_id != session.organization.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    try:
        claimed_ticket = service.claim(ticket_id, session.user.id)
        _record_ticket_event(
            db,
            session,
            action="TICKET_CLAIMED",
            ticket=claimed_ticket,
            details={"assignee_id": claimed_ticket.assigned_to},
        )
        return claimed_ticket
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.post(
    "/{ticket_id}/resolve",
    response_model=TicketResponse,
)
def resolve_ticket(
    ticket_id: str,
    db: Session = Depends(get_db),
    session: AuthenticatedSession = Depends(get_current_session),
):
    require_role(
        session,
        MembershipRole.ORGANIZATION_ADMIN,
        MembershipRole.MANAGER,
        MembershipRole.AGENT,
    )
    service = get_ticket_service(db)
    ticket = service.get(ticket_id)

    if ticket is None or ticket.organization_id != session.organization.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    try:
        resolved_ticket = service.resolve(
            ticket_id,
            session.user.id,
            may_resolve_any_ticket=session.role in {
                MembershipRole.ORGANIZATION_ADMIN,
                MembershipRole.MANAGER,
            },
        )
        _record_ticket_event(
            db,
            session,
            action="TICKET_RESOLVED",
            ticket=resolved_ticket,
        )
        return resolved_ticket
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


def _record_ticket_event(
    db: Session,
    session: AuthenticatedSession,
    *,
    action: str,
    ticket: Ticket,
    details: dict | None = None,
) -> None:
    AuditService(db).record(
        organization_id=session.organization.id,
        actor_id=session.user.id,
        action=action,
        entity_type="TICKET",
        entity_id=ticket.id,
        details=details,
    )


def _validated_department_id(
    db: Session,
    department_id: str | None,
    organization_id: str,
) -> str | None:
    if department_id is None:
        return None
    department = DepartmentRepository(db).get_in_organization(department_id, organization_id)
    if department is None or not department.is_active:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Department not found")
    return department.id


@router.post(
    "/{ticket_id}/predict",
    response_model=TicketPredictionResponse,
)
def predict_ticket(
    ticket_id: str,
    db: Session = Depends(get_db),
    session: AuthenticatedSession = Depends(get_current_session),
):
    require_role(
        session,
        MembershipRole.ORGANIZATION_ADMIN,
        MembershipRole.MANAGER,
        MembershipRole.AGENT,
    )
    ticket = TicketRepository(db).get_by_id(ticket_id)
    if ticket is None or ticket.organization_id != session.organization.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    department_name = None
    if ticket.department_id is not None:
        department = DepartmentRepository(db).get_in_organization(
            ticket.department_id,
            session.organization.id,
        )
        department_name = department.name if department is not None else None

    prediction = TicketPredictionService(db).predict(ticket, department_name)
    AuditService(db).record(
        organization_id=session.organization.id,
        actor_id=session.user.id,
        action="TICKET_PREDICTED",
        entity_type="PREDICTION",
        entity_id=str(prediction.id),
        details={
            "ticket_id": ticket.id,
            "priority": prediction.predicted_priority,
            "confidence": prediction.confidence_score,
        },
    )
    return prediction


@router.post(
    "/{ticket_id}/predictions/{prediction_id}/override",
    response_model=TicketPredictionResponse,
)
def override_prediction(
    ticket_id: str,
    prediction_id: int,
    payload: TicketPredictionOverride,
    db: Session = Depends(get_db),
    session: AuthenticatedSession = Depends(get_current_session),
):
    require_role(
        session,
        MembershipRole.ORGANIZATION_ADMIN,
        MembershipRole.MANAGER,
        MembershipRole.AGENT,
    )
    ticket = TicketRepository(db).get_by_id(ticket_id)
    prediction = db.get(Prediction, prediction_id)
    if (
        ticket is None
        or ticket.organization_id != session.organization.id
        or prediction is None
        or prediction.ticket_id != ticket.id
        or prediction.organization_id != session.organization.id
    ):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prediction not found")

    if session.role == MembershipRole.AGENT and ticket.assigned_to != session.user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Agents may only override predictions for tickets assigned to them",
        )

    department_id = payload.department_id
    if department_id is not None:
        department_id = _validated_department_id(db, department_id, session.organization.id)

    try:
        prediction = TicketPredictionService(db).override(
            prediction,
            ticket,
            priority=payload.priority,
            department_id=department_id,
            overridden_by=session.user.id,
        )
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    AuditService(db).record(
        organization_id=session.organization.id,
        actor_id=session.user.id,
        action="PREDICTION_OVERRIDDEN",
        entity_type="PREDICTION",
        entity_id=str(prediction.id),
        details={
            "ticket_id": ticket.id,
            "priority": payload.priority.value,
            "department_id": department_id,
        },
    )
    return prediction
