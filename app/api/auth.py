from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.db.database import SessionLocal

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