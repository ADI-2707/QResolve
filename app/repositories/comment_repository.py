from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Comment

from .base_repository import BaseRepository


class CommentRepository(BaseRepository[Comment]):
    def __init__(self, db: Session):
        super().__init__(db=db, model=Comment)

    def list_by_ticket(self, organization_id: str, ticket_id: str) -> list[Comment]:
        return list(
            self.db.execute(
                select(Comment)
                .where(
                    Comment.organization_id == organization_id,
                    Comment.ticket_id == ticket_id,
                )
                .order_by(Comment.created_at.asc())
            )
            .scalars()
            .all()
        )
