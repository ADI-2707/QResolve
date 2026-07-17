from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_session
from app.core.authorization import AuthenticatedSession, require_role
from app.db.database import get_db
from app.models import MembershipRole
from app.repositories.comment_repository import CommentRepository
from app.repositories.ticket_repository import TicketRepository
from app.schemas.comment import CommentCreate, CommentResponse
from app.services.audit_service import AuditService
from app.services.comment_service import CommentService


router = APIRouter(prefix="/tickets/{ticket_id}/comments", tags=["Comments"])


def get_comment_service(db: Session = Depends(get_db)) -> CommentService:
    return CommentService(CommentRepository(db))


def _get_tenant_ticket(db: Session, ticket_id: str, session: AuthenticatedSession):
    ticket = TicketRepository(db).get_by_id(ticket_id)
    if ticket is None or ticket.organization_id != session.organization.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return ticket


@router.get("", response_model=list[CommentResponse])
def list_comments(
    ticket_id: str,
    db: Session = Depends(get_db),
    service: CommentService = Depends(get_comment_service),
    session: AuthenticatedSession = Depends(get_current_session),
):
    _get_tenant_ticket(db, ticket_id, session)
    return service.list_by_ticket(session.organization.id, ticket_id)


@router.post("", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    ticket_id: str,
    payload: CommentCreate,
    db: Session = Depends(get_db),
    service: CommentService = Depends(get_comment_service),
    session: AuthenticatedSession = Depends(get_current_session),
):
    require_role(
        session,
        MembershipRole.ORGANIZATION_ADMIN,
        MembershipRole.MANAGER,
        MembershipRole.AGENT,
    )
    _get_tenant_ticket(db, ticket_id, session)
    comment = service.create(
        organization_id=session.organization.id,
        ticket_id=ticket_id,
        user_id=session.user.id,
        content=payload.content,
    )
    AuditService(db).record(
        organization_id=session.organization.id,
        actor_id=session.user.id,
        action="COMMENT_CREATED",
        entity_type="COMMENT",
        entity_id=comment.id,
        details={"ticket_id": ticket_id},
    )
    return comment
