import uuid
from enum import Enum

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.sql import func

from app.db.database import Base


class UserRole(str, Enum):
    PLATFORM_ADMIN = "PLATFORM_ADMIN"
    ORGANIZATION_ADMIN = "ORGANIZATION_ADMIN"
    AGENT = "AGENT"


class UserStatus(str, Enum):
    INVITED = "INVITED"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    ARCHIVED = "ARCHIVED"


class User(Base):
    __tablename__ = "users"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    organization_id = Column(
        String(36),
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )

    first_name = Column(
        String(100),
        nullable=False,
    )

    last_name = Column(
        String(100),
        nullable=False,
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    role = Column(
        SqlEnum(UserRole),
        nullable=False,
        default=UserRole.AGENT,
    )

    status = Column(
        SqlEnum(UserStatus),
        nullable=False,
        default=UserStatus.INVITED,
    )

    last_login = Column(
        DateTime(timezone=True),
        nullable=True,
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