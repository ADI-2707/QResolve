from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    User,
    UserStatus,
)

from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):

    def __init__(
        self,
        db: Session,
    ):
        super().__init__(
            db=db,
            model=User,
        )

    def get_by_email(
        self,
        email: str,
    ) -> User | None:

        statement = (
            select(User)
            .where(
                User.email == email,
            )
        )

        return (
            self.db.execute(statement)
            .scalar_one_or_none()
        )

    def exists_by_email(
        self,
        email: str,
    ) -> bool:

        return (
            self.get_by_email(email)
            is not None
        )

    def list_by_organization(
        self,
        organization_id: str,
    ) -> list[User]:

        statement = (
            select(User)
            .where(
                User.organization_id == organization_id,
                User.status != UserStatus.ARCHIVED,
            )
            .order_by(
                User.first_name,
            )
        )

        return list(
            self.db.execute(statement)
            .scalars()
            .all()
        )

    def update_last_login(
        self,
        user: User,
    ) -> User:

        user.last_login = datetime.utcnow()

        self.db.flush()
        self.db.refresh(user)

        return user

    def archive(
        self,
        user: User,
    ) -> User:

        user.status = UserStatus.ARCHIVED
        user.archived_at = datetime.utcnow()

        self.db.flush()
        self.db.refresh(user)

        return user