import uuid
from enum import Enum

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import String
from sqlalchemy.sql import func

from app.db.database import Base


class OrganizationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    ARCHIVED = "ARCHIVED"


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    name = Column(
        String(150),
        nullable=False,
    )

    slug = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    status = Column(
        SqlEnum(OrganizationStatus),
        nullable=False,
        default=OrganizationStatus.ACTIVE,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    archived_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    retention_until = Column(
        DateTime(timezone=True),
        nullable=True,
    )