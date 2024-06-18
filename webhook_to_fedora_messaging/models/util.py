# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later


from sqlalchemy import Column, UnicodeText
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import FunctionElement
from sqlalchemy.types import DateTime as SQLDateTime

from uuid import uuid4


class utcnow(FunctionElement):
    """
    Current timestamp in UTC for SQL expressions
    """
    type = SQLDateTime
    inherit_cache = True


@compiles(utcnow, "postgresql")
def _postgresql_utcnow(element, compiler, **kwargs):
    return "(NOW() AT TIME ZONE 'utc')"


class UUIDCreatableMixin:
    """
    An SQLAlchemy mixin to automatically generate a custom 8-digit UUID string
    """

    uuid = Column("uuid", UnicodeText, unique=True, nullable=False, default=uuid4().hex[0:8])


class CreatableMixin:
    """
    An SQLAlchemy mixin to store the time when an entity was created
    """

    creation_date = Column("creation_date", SQLDateTime, nullable=False, server_default=utcnow())
