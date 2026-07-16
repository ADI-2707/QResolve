from typing import Generic
from typing import TypeVar

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
        return self.repository.create(entity)

    def get_by_id(
        self,
        entity_id,
    ) -> T | None:
        return self.repository.get_by_id(entity_id)

    def list(
        self,
    ) -> list[T]:
        return self.repository.list()

    def update(
        self,
        entity: T,
    ) -> T:
        return self.repository.update(entity)

    def delete(
        self,
        entity: T,
    ) -> None:
        self.repository.delete(entity)