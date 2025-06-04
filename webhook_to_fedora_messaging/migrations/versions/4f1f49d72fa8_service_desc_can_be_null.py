# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Service.desc can be null

Revision ID: 4f1f49d72fa8
Revises: 6c01198723a8
Create Date: 2024-08-22 11:29:19.880261

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy_helpers.manager import is_sqlite


# revision identifiers, used by Alembic.
revision = "4f1f49d72fa8"
down_revision = "6c01198723a8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()
    if is_sqlite(connection):
        connection.execute(sa.text("PRAGMA foreign_keys=OFF"))
    with op.batch_alter_table("services") as batch_op:
        batch_op.alter_column("desc", existing_type=sa.TEXT(), nullable=True)


def downgrade() -> None:
    connection = op.get_bind()
    if is_sqlite(connection):
        connection.execute(sa.text("PRAGMA foreign_keys=OFF"))
    with op.batch_alter_table("services") as batch_op:
        batch_op.alter_column("desc", existing_type=sa.TEXT(), nullable=False)
