"""add manager and viewer membership roles

Revision ID: 8c04c7489f11
Revises: 25876336a9c6
Create Date: 2026-07-17
"""

from alembic import op


revision = "8c04c7489f11"
down_revision = "25876336a9c6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Extend the PostgreSQL enum; SQLite stores enum values as text."""
    if op.get_bind().dialect.name == "postgresql":
        op.execute("ALTER TYPE membershiprole ADD VALUE IF NOT EXISTS 'MANAGER'")
        op.execute("ALTER TYPE membershiprole ADD VALUE IF NOT EXISTS 'VIEWER'")


def downgrade() -> None:
    """PostgreSQL enum values cannot be safely removed in place."""
