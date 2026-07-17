from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AuditLog

from .base_repository import BaseRepository


class AuditLogRepository(BaseRepository[AuditLog]):
    def __init__(self, db: Session):
        super().__init__(db=db, model=AuditLog)

    def list_by_organization(
        self,
        organization_id: str,
        *,
        page: int,
        page_size: int,
    ) -> list[AuditLog]:
        statement = (
            select(AuditLog)
            .where(AuditLog.organization_id == organization_id)
            .order_by(AuditLog.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        return list(self.db.execute(statement).scalars().all())
