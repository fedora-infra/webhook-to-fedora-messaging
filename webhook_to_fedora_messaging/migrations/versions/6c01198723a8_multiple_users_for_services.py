# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Multiple users for services

Revision ID: 6c01198723a8
Revises: 7d4bba864a99
Create Date: 2024-08-20 07:24:27.637579

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "6c01198723a8"
down_revision = "7d4bba864a99"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "owners",
        sa.Column("service_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["service_id"], ["services.id"], name=op.f("fk_owners_service_id_services")
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_owners_user_id_users")),
        sa.PrimaryKeyConstraint("service_id", "user_id", name=op.f("pk_owners")),
    )
    with op.batch_alter_table("services") as batch_op:
        batch_op.drop_constraint("fk_services_user_id_users", type_="foreignkey")
        batch_op.drop_column("user_id")


def downgrade() -> None:
    op.drop_table("owners")
    op.add_column("services", sa.Column("user_id", sa.INTEGER(), nullable=False))
    op.create_foreign_key(
        "fk_services_user_id_users", "services", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
