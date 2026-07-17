from app.core.security import hash_password

from app.models import (
    User,
    UserStatus,
)

from app.repositories import UserRepository

from .base_service import BaseService


class UserService(
    BaseService[User],
):

    def __init__(
        self,
        repository: UserRepository,
    ):
        super().__init__(repository)

    def create(
        self,
        organization_id: str,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
    ) -> User:

        if self.repository.exists_by_email(
            email,
        ):
            raise ValueError(
                "Email already exists"
            )

        user = User(
            organization_id=organization_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=hash_password(
                password,
            ),
            status=UserStatus.INVITED,
        )

        return super().create(
            user,
        )

    def get(
        self,
        user_id: str,
    ) -> User | None:

        return self.get_by_id(
            user_id,
        )

    def list_by_organization(
        self,
        organization_id: str,
    ) -> list[User]:

        return self.repository.list_by_organization(
            organization_id,
        )

    def archive(
        self,
        user_id: str,
    ) -> User | None:

        user = self.get_by_id(
            user_id,
        )

        if user is None:

            return None

        try:

            user = self.repository.archive(
                user,
            )

            self.repository.db.commit()

            self.repository.db.refresh(
                user,
            )

            return user

        except Exception:

            self.repository.db.rollback()

            raise