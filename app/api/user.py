from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.db.database import SessionLocal

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


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



def get_user_service(
    db: Session = Depends(get_db),
):

    repository = UserRepository(
        db
    )

    return UserService(
        repository
    )



@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    payload: UserCreate,
    service: UserService = Depends(
        get_user_service
    ),
):

    try:

        return service.create(
            organization_id=payload.organization_id,
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
    service: UserService = Depends(
        get_user_service
    ),
):

    user = service.get(
        user_id
    )

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user



@router.get(
    "/organization/{organization_id}",
    response_model=list[UserResponse],
)
def list_users_by_organization(
    organization_id: str,
    service: UserService = Depends(
        get_user_service
    ),
):

    return service.list_by_organization(
        organization_id
    )



@router.delete(
    "/{user_id}",
    response_model=UserResponse,
)
def archive_user(
    user_id: str,
    service: UserService = Depends(
        get_user_service
    ),
):

    user = service.archive(
        user_id
    )

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user