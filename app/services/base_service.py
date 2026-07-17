from typing import Generic
from typing import TypeVar

from sqlalchemy.exc import SQLAlchemyError

from app.repositories.base_repository import BaseRepository

T = TypeVar("T")


class BaseService(Generic[T]):

    def __init__(
        self,
        repository: BaseRepository[T],
    ):
        self.repository = repository

    def create(
        self,
        entity: T,
    ) -> T:

        try:
            entity = self.repository.create(entity)

            self.repository.db.commit()

            self.repository.db.refresh(entity)

            return entity

        except SQLAlchemyError:

            self.repository.db.rollback()

            raise

    def get_by_id(
        self,
        entity_id: str,
    ) -> T | None:

        return self.repository.get_by_id(
            entity_id,
        )

    def list(
        self,
    ) -> list[T]:

        return self.repository.list()

    def update(
        self,
        entity: T,
    ) -> T:

        try:
            entity = self.repository.update(entity)

            self.repository.db.commit()

            self.repository.db.refresh(entity)

            return entity

        except SQLAlchemyError:

            self.repository.db.rollback()

            raise