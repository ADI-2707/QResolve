from app.core.security import (
    create_access_token,
    verify_password,
)

from app.repositories import UserRepository


class AuthService:

    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository

    def login(
        self,
        email: str,
        password: str,
    ) -> str:

        user = self.repository.get_by_email(
            email,
        )

        if user is None:
            raise ValueError(
                "Invalid credentials",
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise ValueError(
                "Invalid credentials",
            )

        self.repository.update_last_login(
            user,
        )

        self.repository.db.commit()

        return create_access_token(
            user.id,
        )