from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_session
from app.core.authorization import AuthenticatedSession, require_role
from app.db.database import get_db
from app.models import MembershipRole
from app.schemas.membership import MembershipResponse, MembershipRoleUpdate
from app.services.audit_service import AuditService
from app.services.membership_administration_service import MembershipAdministrationService


router = APIRouter(prefix="/memberships", tags=["Memberships"])


def get_service(db: Session = Depends(get_db)) -> MembershipAdministrationService:
    return MembershipAdministrationService(db)


@router.get("", response_model=list[MembershipResponse])
def list_memberships(
    service: MembershipAdministrationService = Depends(get_service),
    session: AuthenticatedSession = Depends(get_current_session),
):
    require_role(session, MembershipRole.ORGANIZATION_ADMIN)
    return service.list_by_organization(session.organization.id)


@router.patch("/{membership_id}/role", response_model=MembershipResponse)
def change_role(
    membership_id: str,
    payload: MembershipRoleUpdate,
    service: MembershipAdministrationService = Depends(get_service),
    session: AuthenticatedSession = Depends(get_current_session),
):
    require_role(session, MembershipRole.ORGANIZATION_ADMIN)
    membership = _get_scoped_membership(service, membership_id, session)
    if membership.user_id == session.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot change your own role")

    try:
        membership = service.change_role(membership, payload.role)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    _record_membership_event(
        service.db,
        session,
        action="MEMBERSHIP_ROLE_CHANGED",
        membership_id=membership.id,
        details={"role": membership.role.value},
    )
    return membership


@router.post("/{membership_id}/suspend", response_model=MembershipResponse)
def suspend_membership(
    membership_id: str,
    service: MembershipAdministrationService = Depends(get_service),
    session: AuthenticatedSession = Depends(get_current_session),
):
    require_role(session, MembershipRole.ORGANIZATION_ADMIN)
    membership = _get_scoped_membership(service, membership_id, session)
    if membership.user_id == session.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot suspend your own membership")

    try:
        membership = service.suspend(membership)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    _record_membership_event(service.db, session, action="MEMBERSHIP_SUSPENDED", membership_id=membership.id)
    return membership


@router.post("/{membership_id}/activate", response_model=MembershipResponse)
def activate_membership(
    membership_id: str,
    service: MembershipAdministrationService = Depends(get_service),
    session: AuthenticatedSession = Depends(get_current_session),
):
    require_role(session, MembershipRole.ORGANIZATION_ADMIN)
    membership = _get_scoped_membership(service, membership_id, session)

    try:
        membership = service.activate(membership)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    _record_membership_event(service.db, session, action="MEMBERSHIP_ACTIVATED", membership_id=membership.id)
    return membership


def _get_scoped_membership(
    service: MembershipAdministrationService,
    membership_id: str,
    session: AuthenticatedSession,
):
    membership = service.get_in_organization(membership_id, session.organization.id)
    if membership is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membership not found")
    return membership


def _record_membership_event(
    db: Session,
    session: AuthenticatedSession,
    *,
    action: str,
    membership_id: str,
    details: dict | None = None,
) -> None:
    AuditService(db).record(
        organization_id=session.organization.id,
        actor_id=session.user.id,
        action=action,
        entity_type="MEMBERSHIP",
        entity_id=membership_id,
        details=details,
    )
