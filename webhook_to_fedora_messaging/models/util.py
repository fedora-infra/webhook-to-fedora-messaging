# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later


from datetime import datetime, UTC
from functools import partial
from uuid import uuid4

from sqlalchemy import Column, UnicodeText
from sqlalchemy.types import TIMESTAMP


class UUIDCreatableMixin:
    """
    An SQLAlchemy mixin to automatically generate a custom 8-digit UUID string
    """

    uuid = Column("uuid", UnicodeText, unique=True, nullable=False, default=uuid4().hex[0:8])


class CreatableMixin:
    """
    An SQLAlchemy mixin to store the time when an entity was created
    """

    creation_date = Column(
        "creation_date",
        TIMESTAMP(timezone=True),
        nullable=False,
        default=partial(datetime.now, tz=UTC)
    )
