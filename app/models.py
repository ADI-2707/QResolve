from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.sql import func

from app.db.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    text = Column(
        String,
        nullable=False,
    )

    type = Column(
        String,
        nullable=False,
    )

    queue = Column(
        String,
        nullable=False,
    )

    tag_1 = Column(
        String,
        nullable=False,
    )

    tag_2 = Column(
        String,
        nullable=True,
    )

    tag_3 = Column(
        String,
        nullable=True,
    )

    tag_4 = Column(
        String,
        nullable=True,
    )

    predicted_priority = Column(
        String,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )