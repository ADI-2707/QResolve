from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_session
from app.core.authorization import AuthenticatedSession, require_role
from app.db.database import get_db
from app.models import MembershipRole
from app.repositories.department_repository import DepartmentRepository
from app.schemas.department import DepartmentCreate, DepartmentResponse
from app.services.audit_service import AuditService
from app.services.department_service import DepartmentService


router = APIRouter(prefix="/departments", tags=["Departments"])


def get_service(db: Session = Depends(get_db)) -> DepartmentService:
    return DepartmentService(DepartmentRepository(db))


@router.get("", response_model=list[DepartmentResponse])
def list_departments(
    service: DepartmentService = Depends(get_service),
    session: AuthenticatedSession = Depends(get_current_session),
):
    return service.repository.list_active(session.organization.id)


@router.post("", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(
    payload: DepartmentCreate,
    service: DepartmentService = Depends(get_service),
    session: AuthenticatedSession = Depends(get_current_session),
):
    require_role(session, MembershipRole.ORGANIZATION_ADMIN)
    try:
        department = service.create(session.organization.id, payload.name)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error))

    AuditService(service.repository.db).record(
        organization_id=session.organization.id,
        actor_id=session.user.id,
        action="DEPARTMENT_CREATED",
        entity_type="DEPARTMENT",
        entity_id=department.id,
        details={"name": department.name},
    )
    return department


@router.delete("/{department_id}", response_model=DepartmentResponse)
def archive_department(
    department_id: str,
    service: DepartmentService = Depends(get_service),
    session: AuthenticatedSession = Depends(get_current_session),
):
    require_role(session, MembershipRole.ORGANIZATION_ADMIN)
    department = service.repository.get_in_organization(department_id, session.organization.id)
    if department is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    department = service.archive(department)
    AuditService(service.repository.db).record(
        organization_id=session.organization.id,
        actor_id=session.user.id,
        action="DEPARTMENT_ARCHIVED",
        entity_type="DEPARTMENT",
        entity_id=department.id,
    )
    return department
