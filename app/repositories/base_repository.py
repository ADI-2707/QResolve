from typing import Generic, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import Base

ModelType = TypeVar(
    "ModelType",
    bound=Base,
)


class BaseRepository(Generic[ModelType]):

    def __init__(
        self,
        db: Session,
        model: Type[ModelType],
    ):
        self.db = db
        self.model = model

    def create(
        self,
        entity: ModelType,
    ) -> ModelType:

        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)

        return entity

    def get_by_id(
        self,
        entity_id: str,
    ) -> ModelType | None:

        statement = (
            select(self.model)
            .where(
                self.model.id == entity_id,
            )
        )

        return (
            self.db.execute(statement)
            .scalar_one_or_none()
        )

    def list(
        self,
    ) -> list[ModelType]:

        statement = select(self.model)

        return list(
            self.db.execute(statement)
            .scalars()
            .all()
        )

    def update(
        self,
        entity: ModelType,
    ) -> ModelType:

        self.db.flush()
        self.db.refresh(entity)

        return entity

    def delete(
        self,
        entity: ModelType,
    ) -> None:

        self.db.delete(entity)
        self.db.flush()