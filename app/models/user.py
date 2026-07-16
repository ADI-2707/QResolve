import uuid

from enum import Enum
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from sqlalchemy.sql import func

from app.db.database import Base


class UserStatus(str, Enum):

    INVITED = "INVITED"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    ARCHIVED = "ARCHIVED"



class User(Base):

    __tablename__ = "users"


    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )


    organization_id: Mapped[str] = mapped_column(
        ForeignKey(
            "organizations.id"
        ),
        nullable=False,
        index=True,
    )


    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )


    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )


    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )


    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )


    status: Mapped[UserStatus] = mapped_column(
        SqlEnum(UserStatus),
        nullable=False,
        default=UserStatus.INVITED,
    )


    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


    archived_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


    # Relationship
    organization = relationship(
        "Organization",
        back_populates="users",
    )

    created_tickets = relationship(
        "Ticket",
        foreign_keys="Ticket.created_by",
        back_populates="creator",
    )

    assigned_tickets = relationship(
        "Ticket",
        foreign_keys="Ticket.assigned_to",
        back_populates="assignee",
    )