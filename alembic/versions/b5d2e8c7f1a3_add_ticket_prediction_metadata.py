"""add tenant ticket prediction metadata

Revision ID: b5d2e8c7f1a3
Revises: f3c8a1d6b5e9
Create Date: 2026-07-17
"""

import sqlalchemy as sa
from alembic import op


revision = "b5d2e8c7f1a3"
down_revision = "f3c8a1d6b5e9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("predictions") as batch_op:
        batch_op.add_column(sa.Column("organization_id", sa.String(length=36), nullable=True))
        batch_op.add_column(sa.Column("ticket_id", sa.String(length=36), nullable=True))
        batch_op.add_column(sa.Column("predicted_department", sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column("confidence_score", sa.Float(), nullable=True))
        batch_op.add_column(sa.Column("model_version", sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column("overridden", sa.Boolean(), nullable=False, server_default=sa.false()))
        batch_op.add_column(sa.Column("overridden_by", sa.String(length=36), nullable=True))
        batch_op.create_foreign_key("fk_predictions_organization_id_organizations", "organizations", ["organization_id"], ["id"])
        batch_op.create_foreign_key("fk_predictions_ticket_id_tickets", "tickets", ["ticket_id"], ["id"])
        batch_op.create_foreign_key("fk_predictions_overridden_by_users", "users", ["overridden_by"], ["id"])
    op.create_index("ix_predictions_organization_id", "predictions", ["organization_id"])
    op.create_index("ix_predictions_ticket_id", "predictions", ["ticket_id"])


def downgrade() -> None:
    op.drop_index("ix_predictions_ticket_id", table_name="predictions")
    op.drop_index("ix_predictions_organization_id", table_name="predictions")
    with op.batch_alter_table("predictions") as batch_op:
        batch_op.drop_constraint("fk_predictions_overridden_by_users", type_="foreignkey")
        batch_op.drop_constraint("fk_predictions_ticket_id_tickets", type_="foreignkey")
        batch_op.drop_constraint("fk_predictions_organization_id_organizations", type_="foreignkey")
        batch_op.drop_column("overridden_by")
        batch_op.drop_column("overridden")
        batch_op.drop_column("model_version")
        batch_op.drop_column("confidence_score")
        batch_op.drop_column("predicted_department")
        batch_op.drop_column("ticket_id")
        batch_op.drop_column("organization_id")
