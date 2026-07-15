from app.models import User
from app.models import UserStatus

from app.repositories import UserRepository

from app.core.security import hash_password


class UserService:

    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository


    def create(
        self,
        organization_id: str,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
    ) -> User:

        if self.repository.exists_by_email(
            email
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
                password
            ),
            status=UserStatus.INVITED,
        )


        return self.repository.create(
            user
        )


    def get(
        self,
        user_id: str,
    ) -> User | None:

        return self.repository.get_by_id(
            user_id
        )


    def list_by_organization(
        self,
        organization_id: str,
    ) -> list[User]:

        return self.repository.list_by_organization(
            organization_id
        )


    def archive(
        self,
        user_id: str,
    ) -> User | None:

        user = self.repository.get_by_id(
            user_id
        )


        if user is None:
            return None


        return self.repository.archive(
            user
        )