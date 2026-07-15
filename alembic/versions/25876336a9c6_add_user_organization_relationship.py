"""add user organization relationship

Revision ID: 25876336a9c6
Revises: 28bca6c9faf1
Create Date: 2026-07-15
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "25876336a9c6"
down_revision: Union[str, Sequence[str], None] = "28bca6c9faf1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Remove obsolete user role column.

    User roles are now managed through Membership model.
    """

    with op.batch_alter_table(
        "users"
    ) as batch_op:

        batch_op.drop_column(
            "role"
        )


def downgrade() -> None:
    """
    Restore user role column.
    """

    with op.batch_alter_table(
        "users"
    ) as batch_op:

        batch_op.add_column(
            sa.Column(
                "role",
                sa.String(length=18),
                nullable=False,
                server_default="MEMBER",
            )
        )