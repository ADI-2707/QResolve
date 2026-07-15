from app.repositories import UserRepository

from app.core.security import (
    verify_password,
    create_access_token,
)


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
    ):


        user = self.repository.get_by_email(
            email
        )


        if user is None:

            raise ValueError(
                "Invalid credentials"
            )


        if not verify_password(
            password,
            user.password_hash,
        ):

            raise ValueError(
                "Invalid credentials"
            )


        token = create_access_token(
            user.id
        )


        return token