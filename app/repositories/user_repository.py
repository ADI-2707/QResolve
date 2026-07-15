from datetime import datetime

from sqlalchemy.orm import Session

from app.models import User
from app.models import UserStatus


class UserRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db


    def create(
        self,
        user: User,
    ) -> User:

        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)

        return user


    def get_by_id(
        self,
        user_id: str,
    ) -> User | None:

        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )


    def get_by_email(
        self,
        email: str,
    ) -> User | None:

        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
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

        return (
            self.db.query(User)
            .filter(
                User.organization_id == organization_id,
                User.status != UserStatus.ARCHIVED,
            )
            .order_by(
                User.first_name
            )
            .all()
        )


    def update(
        self,
        user: User,
    ) -> User:

        self.db.flush()
        self.db.refresh(user)

        return user


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