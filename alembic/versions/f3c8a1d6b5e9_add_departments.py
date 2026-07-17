"""add departments and ticket routing

Revision ID: f3c8a1d6b5e9
Revises: e8b2c6d1a9f4
Create Date: 2026-07-17
"""

import sqlalchemy as sa
from alembic import op


revision = "f3c8a1d6b5e9"
down_revision = "e8b2c6d1a9f4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "departments",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("organization_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "slug", name="uq_departments_organization_slug"),
    )
    op.create_index("ix_departments_organization_id", "departments", ["organization_id"])

    with op.batch_alter_table("tickets") as batch_op:
        batch_op.add_column(sa.Column("department_id", sa.String(length=36), nullable=True))
        batch_op.create_foreign_key(
            "fk_tickets_department_id_departments",
            "departments",
            ["department_id"],
            ["id"],
        )
    op.create_index("ix_tickets_department_id", "tickets", ["department_id"])


def downgrade() -> None:
    op.drop_index("ix_tickets_department_id", table_name="tickets")
    with op.batch_alter_table("tickets") as batch_op:
        batch_op.drop_constraint("fk_tickets_department_id_departments", type_="foreignkey")
        batch_op.drop_column("department_id")
    op.drop_index("ix_departments_organization_id", table_name="departments")
    op.drop_table("departments")
