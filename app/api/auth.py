from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.api.dependencies import get_current_user

from app.models import User
from app.repositories import UserRepository
from app.services import AuthService

from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
)


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



def get_auth_service(
    db: Session = Depends(get_db),
):

    repository = UserRepository(
        db
    )

    return AuthService(
        repository
    )



@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    payload: LoginRequest,
    service: AuthService = Depends(
        get_auth_service
    ),
):

    try:

        token = service.login(
            email=payload.email,
            password=payload.password,
        )


        return TokenResponse(
            access_token=token
        )


    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        )


@router.get(
    "/me",
)
def get_me(
    current_user: User = Depends(
        get_current_user,
    ),
):

    return {
        "id": current_user.id,
        "organization_id": current_user.organization_id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "status": current_user.status,
    }