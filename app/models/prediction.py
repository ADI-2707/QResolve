from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
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

    organization_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("organizations.id"),
        nullable=True,
        index=True,
    )

    ticket_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("tickets.id"),
        nullable=True,
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

    predicted_department: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    confidence_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    model_version: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    overridden: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    overridden_by: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("users.id"),
        nullable=True,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
