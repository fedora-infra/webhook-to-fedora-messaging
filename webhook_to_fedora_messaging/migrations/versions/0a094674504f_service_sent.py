# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Service.sent

Revision ID: 0a094674504f
Revises: initial
Create Date: 2024-08-13 07:25:18.654617

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "0a094674504f"
down_revision = "initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("services", sa.Column("sent", sa.Integer(), nullable=False, default=0))


def downgrade() -> None:
    op.drop_column("services", "sent")
