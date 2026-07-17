from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Invitation

from .base_repository import BaseRepository


class InvitationRepository(BaseRepository[Invitation]):
    def __init__(self, db: Session):
        super().__init__(db=db, model=Invitation)

    def get_by_token_hash(self, token_hash: str) -> Invitation | None:
        return self.db.execute(
            select(Invitation).where(Invitation.token_hash == token_hash)
        ).scalar_one_or_none()

    def get_pending_by_email(self, organization_id: str, email: str) -> Invitation | None:
        return self.db.execute(
            select(Invitation).where(
                Invitation.organization_id == organization_id,
                Invitation.email == email,
                Invitation.accepted_at.is_(None),
            )
        ).scalar_one_or_none()
