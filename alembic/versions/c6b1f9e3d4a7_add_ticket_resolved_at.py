"""add ticket resolved timestamp

Revision ID: c6b1f9e3d4a7
Revises: a1f95c2e68b2
Create Date: 2026-07-17
"""

import sqlalchemy as sa
from alembic import op


revision = "c6b1f9e3d4a7"
down_revision = "a1f95c2e68b2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("tickets") as batch_op:
        batch_op.add_column(sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("tickets") as batch_op:
        batch_op.drop_column("resolved_at")
