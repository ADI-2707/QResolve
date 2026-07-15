from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from app.db.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    text: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    type: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    queue: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    tag_1: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    tag_2: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    tag_3: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    tag_4: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    predicted_priority: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )