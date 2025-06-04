# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Remove User.uuid

Revision ID: 7d4bba864a99
Revises: 0a094674504f
Create Date: 2024-08-13 17:33:34.953271

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "7d4bba864a99"
down_revision = "0a094674504f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_constraint("uq_users_uuid", type_="unique")
        batch_op.drop_column("uuid")


def downgrade() -> None:
    op.add_column("users", sa.Column("uuid", sa.TEXT(), nullable=False))
    op.create_unique_constraint("uq_users_uuid", "users", ["uuid"])
