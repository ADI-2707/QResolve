"""preserve migration history after membership introduction

Revision ID: 25876336a9c6
Revises: 28bca6c9faf1
Create Date: 2026-07-15
"""

from typing import Sequence, Union

from alembic import op


revision: str = "25876336a9c6"
down_revision: Union[str, Sequence[str], None] = "28bca6c9faf1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """The initial schema already stores roles in memberships."""


def downgrade() -> None:
    """No schema change is required when downgrading this compatibility revision."""
