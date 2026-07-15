from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.repositories import OrganizationRepository
from app.services import OrganizationService

from app.schemas.organization import (
    OrganizationCreate,
    OrganizationResponse,
)


router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



def get_organization_service(
    db: Session = Depends(get_db),
):

    repository = OrganizationRepository(
        db
    )

    return OrganizationService(
        repository
    )



@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_organization(
    payload: OrganizationCreate,
    service: OrganizationService = Depends(
        get_organization_service
    ),
):

    return service.create(
        payload.name
    )