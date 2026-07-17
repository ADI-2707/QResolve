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
from app.models import MembershipRole
from app.repositories import UserRepository
from app.services import UserService

from app.schemas.user import (
    UserCreate,
    UserResponse,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def get_user_service(
    db: Session = Depends(get_db),
) -> UserService:

    repository = UserRepository(db)

    return UserService(repository)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
    session: AuthenticatedSession = Depends(get_current_session),
):
    require_role(session, MembershipRole.ORGANIZATION_ADMIN)
    try:
        return service.create(
            organization_id=session.organization.id,
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            password=payload.password,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
    session: AuthenticatedSession = Depends(get_current_session),
):

    if session.role != MembershipRole.ORGANIZATION_ADMIN and user_id != session.user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    user = service.get(user_id)

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if user.organization_id != session.organization.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@router.get(
    "/organization/{organization_id}",
    response_model=list[UserResponse],
)
def list_users_by_organization(
    organization_id: str,
    service: UserService = Depends(get_user_service),
    session: AuthenticatedSession = Depends(get_current_session),
):
    require_role(session, MembershipRole.ORGANIZATION_ADMIN)

    if organization_id != session.organization.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    return service.list_by_organization(
        session.organization.id
    )


@router.delete(
    "/{user_id}",
    response_model=UserResponse,
)
def archive_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
    session: AuthenticatedSession = Depends(get_current_session),
):
    require_role(session, MembershipRole.ORGANIZATION_ADMIN)

    user = service.get(user_id)
    if user is not None and user.organization_id != session.organization.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user = service.archive(
        user_id
    )

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user
