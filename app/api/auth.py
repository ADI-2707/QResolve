from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.api.dependencies import get_current_session
from app.core.authorization import AuthenticatedSession
from app.core.security import hash_password, verify_password
from app.core.sessions import create_session_response

from app.models import (
    Membership,
    MembershipRole,
    MembershipStatus,
    Organization,
    OrganizationStatus,
    User,
    UserStatus,
)
from app.schemas.session import BootstrapRequest, LoginPayload, SessionResponse
from app.schemas.session import InvitationAcceptance
from app.services.invitation_service import InvitationService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)



def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



@router.post(
    "/bootstrap",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def bootstrap(payload: BootstrapRequest, db: Session = Depends(get_db)):
    """Create an organization and its first active organization administrator."""
    if db.query(User).filter(User.email == payload.email).first() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    slug = payload.organization_name.lower().replace(" ", "-")
    slug = "".join(character for character in slug if character.isalnum() or character == "-").strip("-")
    if not slug:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Organization name cannot generate a valid slug")
    if db.query(Organization).filter(Organization.slug == slug).first() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Organization name is already in use")

    try:
        organization = Organization(name=payload.organization_name, slug=slug, status=OrganizationStatus.ACTIVE)
        db.add(organization)
        db.flush()

        user = User(
            organization_id=organization.id,
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            password_hash=hash_password(payload.password),
            status=UserStatus.ACTIVE,
        )
        db.add(user)
        db.flush()

        membership = Membership(
            organization_id=organization.id,
            user_id=user.id,
            role=MembershipRole.ORGANIZATION_ADMIN,
            status=MembershipStatus.ACTIVE,
        )
        db.add(membership)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return create_session_response(user, organization, membership)


@router.post("/login", response_model=SessionResponse)
def login(payload: LoginPayload, db: Session = Depends(get_db)):
    organization = db.query(Organization).filter(Organization.slug == payload.organization_slug).first()
    if organization is None or organization.status != OrganizationStatus.ACTIVE:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    user = db.query(User).filter(User.email == payload.email, User.organization_id == organization.id).first()
    if user is None or user.status != UserStatus.ACTIVE or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    membership = db.execute(
        select(Membership).where(
            Membership.user_id == user.id,
            Membership.organization_id == organization.id,
            Membership.status == MembershipStatus.ACTIVE,
        )
    ).scalar_one_or_none()
    if membership is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    user.last_login = datetime.utcnow()
    db.commit()
    return create_session_response(user, organization, membership)


@router.post("/invitations/accept", response_model=SessionResponse)
def accept_invitation(
    payload: InvitationAcceptance,
    db: Session = Depends(get_db),
):
    try:
        user, membership = InvitationService(db).accept(
            token=payload.token,
            first_name=payload.first_name,
            last_name=payload.last_name,
            password=payload.password,
        )
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    organization = db.get(Organization, membership.organization_id)
    if organization is None or organization.status != OrganizationStatus.ACTIVE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Organization is unavailable")
    return create_session_response(user, organization, membership)


@router.get(
    "/me",
)
def get_me(
    session: AuthenticatedSession = Depends(get_current_session),
):
    return {
        "id": session.user.id,
        "organization_id": session.organization.id,
        "organization_slug": session.organization.slug,
        "first_name": session.user.first_name,
        "last_name": session.user.last_name,
        "email": session.user.email,
        "status": session.user.status,
        "role": session.role,
    }
