from sqlalchemy.exc import SQLAlchemyError

from app.models import Comment
from app.repositories.comment_repository import CommentRepository


class CommentService:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    def create(
        self,
        *,
        organization_id: str,
        ticket_id: str,
        user_id: str,
        content: str,
    ) -> Comment:
        try:
            comment = Comment(
                organization_id=organization_id,
                ticket_id=ticket_id,
                user_id=user_id,
                content=content,
            )
            self.repository.db.add(comment)
            self.repository.db.commit()
            self.repository.db.refresh(comment)
            return comment
        except SQLAlchemyError:
            self.repository.db.rollback()
            raise

    def list_by_ticket(self, organization_id: str, ticket_id: str) -> list[Comment]:
        return self.repository.list_by_ticket(organization_id, ticket_id)
