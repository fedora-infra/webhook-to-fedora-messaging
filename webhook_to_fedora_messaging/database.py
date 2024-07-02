# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Use sqlalchemy-helpers.

Import the functions we will use in the main code and in migrations.
"""

from sqlalchemy_helpers import Base, get_or_create, update_or_create, is_sqlite, exists_in_db  # noqa: F401
from sqlalchemy_helpers.flask_ext import DatabaseExtension, get_or_404, first_or_404  # noqa: F401

db = DatabaseExtension()
