from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_session
from app.core.authorization import AuthenticatedSession, require_role
from app.db.database import get_db
from app.models import MembershipRole
from app.repositories.audit_log_repository import AuditLogRepository
from app.schemas.audit import AuditLogListResponse


router = APIRouter(prefix="/audit", tags=["Audit logs"])


@router.get("", response_model=AuditLogListResponse)
def list_audit_logs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    db: Session = Depends(get_db),
    session: AuthenticatedSession = Depends(get_current_session),
):
    require_role(session, MembershipRole.ORGANIZATION_ADMIN)
    events = AuditLogRepository(db).list_by_organization(
        session.organization.id,
        page=page,
        page_size=page_size,
    )
    return AuditLogListResponse(events=events, page=page, page_size=page_size)
