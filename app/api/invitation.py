from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_session
from app.core.authorization import AuthenticatedSession, require_role
from app.db.database import get_db
from app.models import MembershipRole
from app.schemas.session import InvitationCreate, InvitationResponse
from app.services.invitation_service import InvitationService


router = APIRouter(prefix="/invitations", tags=["Invitations"])


@router.post("", response_model=InvitationResponse, status_code=status.HTTP_201_CREATED)
def create_invitation(
    payload: InvitationCreate,
    db: Session = Depends(get_db),
    session: AuthenticatedSession = Depends(get_current_session),
):
    require_role(session, MembershipRole.ORGANIZATION_ADMIN)
    try:
        role = MembershipRole(payload.role)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid membership role")
    if role == MembershipRole.PLATFORM_ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Platform administrators cannot be invited")

    try:
        invitation, token = InvitationService(db).create(
            organization_id=session.organization.id,
            email=str(payload.email),
            role=role,
            invited_by=session.user.id,
        )
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))

    return InvitationResponse(
        id=invitation.id,
        email=invitation.email,
        role=invitation.role.value,
        expires_at=invitation.expires_at,
        invitation_token=token,
    )
