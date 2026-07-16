from typing import Generic
from typing import Type
from typing import TypeVar

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
        self.db.commit()
        self.db.refresh(entity)

        return entity

    def get_by_id(
        self,
        entity_id,
    ) -> ModelType | None:

        return (
            self.db.query(self.model)
            .filter(
                self.model.id == entity_id,
            )
            .first()
        )

    def list(
        self,
    ) -> list[ModelType]:

        return (
            self.db.query(self.model)
            .all()
        )

    def update(
        self,
        entity: ModelType,
    ) -> ModelType:

        self.db.commit()
        self.db.refresh(entity)

        return entity

    def delete(
        self,
        entity: ModelType,
    ) -> None:

        self.db.delete(entity)
        self.db.commit()